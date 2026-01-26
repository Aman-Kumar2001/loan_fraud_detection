
CREATE INDEX idx_sender_id ON transactions(sender_id);
CREATE INDEX idx_receiver_id ON transactions(receiver_id);
CREATE INDEX idx_step ON transactions(step);
