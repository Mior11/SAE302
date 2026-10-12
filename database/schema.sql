-- Schema MariaDB pour la SAÉ 3.02 : simulation pédagogique de carrefour.
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

CREATE TABLE IF NOT EXISTS vehicles (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    vehicle_code VARCHAR(64) NOT NULL,
    vehicle_type ENUM('voiture', 'camion', 'bus', 'ambulance', 'police', 'pompiers', 'autre') NOT NULL DEFAULT 'voiture',
    entry_direction ENUM('nord', 'est', 'sud', 'ouest') NOT NULL,
    destination_direction ENUM('nord', 'est', 'sud', 'ouest') NULL,
    is_emergency BOOLEAN NOT NULL DEFAULT FALSE,
    status ENUM('en_attente', 'en_circulation', 'arrete', 'passe', 'sorti') NOT NULL DEFAULT 'en_attente',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exited_at TIMESTAMP NULL,
    UNIQUE KEY uq_vehicle_session_code (session_id, vehicle_code),
    CONSTRAINT fk_vehicle_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS priority_events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    vehicle_id BIGINT UNSIGNED NULL,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    direction ENUM('nord', 'est', 'sud', 'ouest') NOT NULL,
    duration_ms INT UNSIGNED NULL,
    outcome ENUM('requested', 'accepted', 'rejected', 'completed', 'cancelled', 'timeout') NOT NULL DEFAULT 'requested',
    details JSON NULL,
    CONSTRAINT fk_priority_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE,
    CONSTRAINT fk_priority_vehicle FOREIGN KEY (vehicle_id)
      REFERENCES vehicles(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS traffic_events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    vehicle_id BIGINT UNSIGNED NULL,
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(64) NOT NULL,
    details JSON NULL,
    CONSTRAINT fk_traffic_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE,
    CONSTRAINT fk_traffic_vehicle FOREIGN KEY (vehicle_id)
      REFERENCES vehicles(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS traffic_lights_log (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNSIGNED NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    direction ENUM('nord', 'est', 'sud', 'ouest') NOT NULL,
    previous_state ENUM('rouge', 'orange', 'vert', 'eteint') NULL,
    new_state ENUM('rouge', 'orange', 'vert', 'eteint') NOT NULL,
    reason ENUM('cycle_normal', 'priorite_urgence', 'retour_normal', 'mode_manuel') NOT NULL DEFAULT 'cycle_normal',
    CONSTRAINT fk_lights_session FOREIGN KEY (session_id)
      REFERENCES simulation_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_sessions_started ON simulation_sessions(started_at);
CREATE INDEX idx_priority_requested ON priority_events(requested_at);
CREATE INDEX idx_traffic_occurred ON traffic_events(occurred_at);
CREATE INDEX idx_lights_changed ON traffic_lights_log(changed_at);
