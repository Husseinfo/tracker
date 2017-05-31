-- auto-generated definition
create function checkinout() returns trigger
	language plpgsql
as $$
BEGIN
  IF new.inout IS NOT NULL
  THEN
    RETURN NULL;
  END IF;
  IF (SELECT COUNT(*)
           FROM tracker_attendance
           WHERE user_id = new.user_id AND date :: DATE = now() :: DATE) = 0
  THEN
    new.inout := TRUE;
  ELSEIF (SELECT DISTINCT ON (date) inout
          FROM tracker_attendance
          WHERE user_id = new.user_id
          ORDER BY date DESC)
    THEN
      new.inout := FALSE;
  ELSE
    new.inout := TRUE;
  END IF;
  RETURN NULL;
END
$$
;

create trigger checkinouttrigger
	before insert
	on tracker_attendance
	for each row
	execute procedure checkinout()
;
