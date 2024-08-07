CREATE DEFINER=`assessment_app`@`%` PROCEDURE `qustions`( IN sub VARCHAR(10),IN lamka VARCHAR(50))
BEGIN
    SELECT fld_total_exp_name, fld_post_applied_for_name, fld_que_type_name, fld_option_name, fld_correct_option_name
    FROM Interviewapp_questionsmaster
    WHERE fld_post_applied_for_name = sub and fld_total_exp_name=lamka;
END