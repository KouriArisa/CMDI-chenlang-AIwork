CREATE TABLE IF NOT EXISTS todo_item (
    id BIGINT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    due_date DATE NULL,
    completed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT todo_item_status_valid
        CHECK (status IN ('pending', 'completed')),
    CONSTRAINT todo_item_priority_valid
        CHECK (priority IN ('low', 'medium', 'high')),
    PRIMARY KEY (id),
    KEY todo_item_status_idx (status),
    KEY todo_item_due_date_idx (due_date)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
