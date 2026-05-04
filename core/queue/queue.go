package queue

import (
	"encoding/json"
	"io/ioutil"
	"path/filepath"
	"time"
)

type Job struct {
	ID         string    `json:"id"`
	Briefing   string    `json:"briefing"`
	Status     string    `json:"status"`
	Progress   int       `json:"progress"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
	ProjectPath string    `json:"project_path"`
	ErrorMsg   string    `json:"error_msg,omitempty"`
}

const queueFile = `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\state\queue.json`

func LoadQueue() ([]Job, error) {
	path := filepath.Clean(queueFile)
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return []Job{}, nil
	}
	var jobs []Job
	if err := json.Unmarshal(data, &jobs); err != nil {
		return nil, err
	}
	return jobs, nil
}

func SaveQueue(jobs []Job) error {
	path := filepath.Clean(queueFile)
	data, err := json.MarshalIndent(jobs, "", "  ")
	if err != nil {
		return err
	}
	return ioutil.WriteFile(path, data, 0644)
}

func AddJob(jobs *[]Job, job Job) {
	*jobs = append(*jobs, job)
}
