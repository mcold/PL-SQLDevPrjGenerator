create or replace package bar.test_pkg is
   
  procedure do_something;

end test_pkg;
/


create or replace package body bar.test_pkg is
   
  procedure do_something
    is
    begin
      dbms_output.put_line('Something is done!');
    end;

end test_pkg;
/