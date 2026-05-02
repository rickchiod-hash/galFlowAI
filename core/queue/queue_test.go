package queue

import (
	"testing"
	"time"
)

func TestAddJob(t *testing.T) {
	jobs := []Job{}
	job := Job{
		ID:         "test1",
		Briefing:   "Test briefing",
		Status:     "pending",
		Progress:   0,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	AddJob(&jobs, job)
	if len(jobs) != 1 {
		t.Errorf("Expected 1 job, got %d", len(jobs))
	}
}
