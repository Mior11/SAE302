-- Schéma de départ pour le prototype SAÉ 3.02.
CREATE DATABASE IF NOT EXISTS sae302_carrefour
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sae302_carrefour;

CREATE TABLE IF NOT EXISTS simulation_sessions (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    junction_type ENUM('4-branches', 'T') NOT NULL DEFAULT '4-branches',
    traffic_level ENUM('fluide', 'modere', 'embouteillage') NOT NULL DEFAULT 'modere',
    regulation ENUM('feux', 'stop', 'priorite_droite') NOT NULL DEFAULT 'feux',
    notes TEXT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS priority_events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    direction ENUM('nord', 'est', 'sud', 'ouest') NOT NULL,
    duration_ms INT UNSIGNED NULL,
    outcome ENUM('accepted', 'rejected', 'completed', 'cancelled') NOT NULL DEFAULT 'accepted',
    CONSTRAINT fk_priority_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS traffic_events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(64) NOT NULL,
    details JSON NULL,
    CONSTRAINT fk_traffic_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;
