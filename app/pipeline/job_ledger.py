"""SQLite WAL job ledger for persistent job state management (PIPE-403)."""

import json
import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

from app.pipeline.job_state import JobState, JobStatus


class SQLiteJobLedger:
    """SQLite-based job ledger with WAL mode for persistent job state storage.

    Provides ACID transactions and crash recovery without requiring Redis.
    """

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the job ledger.

        Args:
            db_path: Path to SQLite database file. Defaults to state/job_ledger.db
        """
        if db_path is None:
            db_path = str(Path(__file__).parent.parent / "state" / "job_ledger.db")

        self.db_path = db_path
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._ensure_directory()
        self._initialize_database()

    def _ensure_directory(self) -> None:
        """Ensure the directory for the database file exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Create a new database connection with WAL mode enabled."""
        conn = sqlite3.connect(
            self.db_path,
            timeout=20.0,
            check_same_thread=False,
            isolation_level=None  # Autocommit mode; we'll manage transactions explicitly
        )
        # Enable WAL mode for better concurrency
        conn.execute("PRAGMA journal_mode=WAL")
        # Ensure foreign keys are enabled
        conn.execute("PRAGMA foreign_keys=ON")
        # Set synchronous mode to NORMAL for good performance with safety
        conn.execute("PRAGMA synchronous=NORMAL")
        # Return rows as dictionary-like objects
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _transaction(self):
        """Context manager for database transactions."""
        with self._lock:
            conn = self._get_connection()
            try:
                yield conn
                conn.commit()
            except Exception as e:
                logger.error("Job ledger transaction failed, rolling back: %s", e)
                conn.rollback()
                raise
            finally:
                conn.close()

    def _initialize_database(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        with self._transaction() as conn:
            # Job states table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_states (
                    job_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    job_type TEXT NOT NULL,
                    params TEXT NOT NULL,  -- JSON string
                    status TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    started_at REAL,
                    completed_at REAL,
                    current_stage TEXT,
                    progress INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    error TEXT,
                    output_path TEXT,
                    metadata TEXT NOT NULL  -- JSON string
                )
            """)

            # Indexes for common queries
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_states_project_id
                ON job_states(project_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_states_status
                ON job_states(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_states_created_at
                ON job_states(created_at)
            """)

            # Queue metadata table (for running job ID and other queue-level state)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS queue_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            # Initialize running job ID if not present
            conn.execute("""
                INSERT OR IGNORE INTO queue_metadata (key, value)
                VALUES ('running_job_id', NULL)
            """)

    def _job_from_row(self, row: sqlite3.Row) -> JobState:
        """Convert a database row to a JobState object."""
        job = JobState(
            job_id=row["job_id"],
            project_id=row["project_id"],
            job_type=row["job_type"],
            params=json.loads(row["params"]) if row["params"] else {}
        )
        job.status = JobStatus(row["status"])
        job.created_at = row["created_at"]
        job.started_at = row["started_at"]
        job.completed_at = row["completed_at"]
        job.current_stage = row["current_stage"]
        job.progress = row["progress"]
        job.message = row["message"]
        job.error = row["error"]
        job.output_path = row["output_path"]
        job.metadata = json.loads(row["metadata"]) if row["metadata"] else {}
        return job

    def save_job(self, job: JobState) -> None:
        """Save or update a job in the ledger."""
        with self._transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO job_states (
                    job_id, project_id, job_type, params, status,
                    created_at, started_at, completed_at, current_stage,
                    progress, message, error, output_path, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.job_id,
                job.project_id,
                job.job_type,
                json.dumps(job.params),
                job.status.value,
                job.created_at,
                job.started_at,
                job.completed_at,
                job.current_stage,
                job.progress,
                job.message,
                job.error,
                job.output_path,
                json.dumps(job.metadata)
            ))

    def load_job(self, job_id: str) -> Optional[JobState]:
        """Load a job by its ID."""
        with self._transaction() as conn:
            cursor = conn.execute(
                "SELECT * FROM job_states WHERE job_id = ?",
                (job_id,)
            )
            row = cursor.fetchone()
            if row:
                return self._job_from_row(row)
            return None

    def load_jobs(
        self,
        project_id: Optional[str] = None,
        status: Optional[JobStatus] = None,
        limit: int = 100
    ) -> List[JobState]:
        """Load jobs with optional filtering."""
        query = "SELECT * FROM job_states WHERE 1=1"
        params: List[Any] = []

        if project_id is not None:
            query += " AND project_id = ?"
            params.append(project_id)

        if status is not None:
            query += " AND status = ?"
            params.append(status.value)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._transaction() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [self._job_from_row(row) for row in rows]

    def delete_job(self, job_id: str) -> bool:
        """Delete a job from the ledger."""
        with self._transaction() as conn:
            cursor = conn.execute(
                "DELETE FROM job_states WHERE job_id = ?",
                (job_id,)
            )
            return cursor.rowcount > 0

    def set_running_job_id(self, job_id: Optional[str]) -> None:
        """Set the currently running job ID in queue metadata."""
        with self._transaction() as conn:
            if job_id is None:
                conn.execute(
                    "UPDATE queue_metadata SET value = NULL WHERE key = 'running_job_id'"
                )
            else:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO queue_metadata (key, value)
                    VALUES ('running_job_id', ?)
                    """,
                    (job_id,)
                )

    def get_running_job_id(self) -> Optional[str]:
        """Get the currently running job ID from queue metadata."""
        with self._transaction() as conn:
            cursor = conn.execute(
                "SELECT value FROM queue_metadata WHERE key = 'running_job_id'"
            )
            row = cursor.fetchone()
            return row[0] if row else None

    def close(self) -> None:
        """Close any open connections (placeholder for connection pooling if needed)."""
        # With our current approach of opening/closing connections per transaction,
        # there's nothing to close here. This method is for interface completeness.
        pass

    def vacuum(self) -> None:
        """Vacuum the database to reclaim space."""
        with self._transaction() as conn:
            conn.execute("VACUUM")


# Global ledger instance for use throughout the application
job_ledger = SQLiteJobLedger()