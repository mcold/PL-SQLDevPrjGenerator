set serveroutput on;
spool &&spool_fn. append

column owner format a24
column object_name format a35
column object_type format a19

begin
  dbms_output.disable;
  dbms_output.enable(100000);
  dbms_output.put_line('Recompiling invalid objects');
  dbms_output.put_line(chr(10));
  for i in 
  (
   select a.object_name, 
          a.owner,
          a.object_type,
          decode(a.object_type, 'PACKAGE', 'PAKAGE BODY', 'TYPE', 'TYPE BODY', a.object_type) as object_to_compile,
          decode(a.object_type, 'PAKAGE BODY', 'COMPILE BODY',  'TYPE BODY',  'COMPILE BODY', 'COMPILE') as type_compile
   from all_objects a
   where a.object_type in ('PACKAGE', 'PAKAGE BODY', 'PROCEDURE', 'VIEW', 'FUNCTION', 'TRIGGER',
                           'TYPE', 'TYPE BODY', 'JAVA CLASS', 'JAVA SOURCE')
     and a.status = 'INVALID'
     and (a.owner in (upper('&&foo.'), upper('&&bar.')))
     order by decode(a.object_type,
                     'FUNCTION',          1,
                     'PROCEDURE',         2,
                     'PACKAGE',           3,
                     'PACKAGE BODY',      4,
                     'VIEW',              5,
                     'MATERIALIZED VIEW', 6,
                     'TRIGGER',           7,
                     'TYPE',              8,
                     'TYPE BODY',         9,
                     'JAVA SOURCE',       10,
                     'JAVA CLASS',        11
                     )
  
  )
  loop
    begin
    execute immediate('alter ' || i.object_to_compile
                               || case when i.object_to_compile in ('JAVA CLASS', 'JAVA SOURCE') then ' "' else ' ' end
                               || i.owner
                               || case when i.object_to_compile in ('JAVA CLASS', 'JAVA SOURCE') then '"' else '' end
                               || '.'
                               || case when i.object_to_compile in ('JAVA CLASS', 'JAVA SOURCE') then '"' else '' end
                               || i.object_name
                               || case when i.object_to_compile in ('JAVA CLASS', 'JAVA SOURCE') then '" ' else ' ' end
                               || i.type_compile);
    dbms_output.put_line(i.object_type|| ' '||i.owner||'.'||i.object_name||' successfully compiled.'||chr(10));
    
    exception when others then
      dbms_output.put_line(i.object_type|| ' '||i.owner||'.'||i.object_name||' compiled with ERRORS.');
      for j in (select text from all_errors where name = i.object_name and type=i.object_type and owner = i.owner
                order by sequence
                )
      loop
        dbms_output.put_line(j.text);
      end loop;
      dbms_output.put_line(chr(10));
  end;            
  end loop;
end;
/

prompt Invalid Oracle objects...
select a.owner, a.object_name, a.object_type from all_objects a where a.status = 'INVALID'
and a.object_type not in ('MATERIALIZED VIEW', 'SYNONYM')
and (a.owner in (upper('&&foo.'), upper('&&bar.')))
order by a.owner, a.object_name, decode(a.object_type,
'FUNCTION',          1,
                     'PROCEDURE',         2,
                     'PACKAGE',           3,
                     'PACKAGE BODY',      4,
                     'VIEW',              5,
                     'MATERIALIZED VIEW', 6,
                     'TRIGGER',           7,
                     'TYPE',              8,
                     'TYPE BODY',         9,
                     'JAVA SOURCE',       10,
                     'JAVA CLASS',        11
                     );
prompt
prompt ==================================================================
prompt

