-- create a table for chats
--create table chats
--    (chat_id NUMERIC,
--    user_id numeric,
--    constraint chats_PK PRIMARY KEY (chat_id));

-- create a table for calculations history
create table calculations
    (id NUMERIC,
    calculation_date_UTC date,
    calculation_time_UTC time,
    antenna_latitude float,
    antenna_longitude float,
    antenna_offset float,
    satellite_longitude float,
    calculated_satellite_azimuth float,
    calculated_sun_azimuth float,
    calculated_true_vertical float,
    calculated_sun_satellite_m45_parity time,
    calculated_sun_satellite_m30_parity time,
    calculated_sun_satellite_parity time,
    calculated_sun_satellite_p30_parity time,
    calculated_sun_satellite_p45_parity time,
    result varchar(100),
    constraint calculations_PK PRIMARY KEY (id));


-- create a table for current dialogs
create table chats
    (chat_id NUMERIC,
    user_id numeric unique,
    current_step numeric not null,
    user_language varchar(10) not null,
    calculation_date date,
    calculation_time time,
    calculation_timezone numeric,
    antenna_latitude float,
    antenna_longitude float,
    antenna_offset float,
    satellite_longitude float,
    calculated_azimuth float,
    calculated_vertical float,
    constraint chats_PK PRIMARY KEY (chat_id));

