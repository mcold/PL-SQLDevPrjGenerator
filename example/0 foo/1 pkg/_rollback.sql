create or replace package foo.test_pkg is
   
  procedure do_something;

end test_pkg;
/


create or replace package body foo.test_pkg is
   
  procedure do_something
    is
    begin
      dbms_output.put_line('Something is returned!');
    end;

end test_pkg;
/