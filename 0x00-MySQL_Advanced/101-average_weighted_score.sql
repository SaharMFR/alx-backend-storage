-- Creates a stored procedure `ComputeAverageWeightedScoreForUsers` that
-- computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users,
        (SELECT users.id, SUM(score * weight) / SUM(weight) AS w_avg
        FROM users
        JOIN corrections ON users.id = corrections.user_id
        JOIN projects ON corrections.project_id = projects.id
        GROUP BY users.id)
    AS WA
    SET users.average_score = WA.w_avg
    WHERE users.id = WA.id;
END $$
DELIMITER ;
