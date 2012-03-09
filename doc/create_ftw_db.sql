-- create database ftw DEFAULT CHARACTER SET utf8;


drop table if exists tests;
create table tests (
    id int(11) NOT NULL AUTO_INCREMENT,
    testid varchar(56) collate utf8_unicode_ci,
    init_time int,
    ftwinit varchar(128),
    PRIMARY KEY (id, testid, init_time),
    UNIQUE KEY id (id),
    UNIQUE KEY testid (testid)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- status: 0 -> virgin 1-> started
drop table if exists schedules;
create table schedules (
    id int(11) NOT NULL AUTO_INCREMENT,
    testid varchar(56) collate utf8_unicode_ci,
    start_time int,
    status int,

    PRIMARY KEY (id, testid),
    UNIQUE KEY id (id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- status: 0 -> UNKNOWN, 1-> seen-OK; 2 -> seen.WARNING; 3 -> seen.CRITICAL; 4 -> not seen; 5 -> dinc-code, cant render 
drop table if exists test_results;
create table test_results (
    id int(11) NOT NULL AUTO_INCREMENT,
    testid varchar(56) collate utf8_unicode_ci,
    account varchar(128),
    status int,
    checked int DEFAULT 0,


    PRIMARY KEY (id, testid),
    UNIQUE KEY id (id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists test_logs;
create table test_logs (
    id int(11) NOT NULL AUTO_INCREMENT,
    testid varchar(56) collate utf8_unicode_ci,
    account varchar(128),
    remarks varchar(1024),

    PRIMARY KEY (id, testid),
    UNIQUE KEY id (id)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists test_logins;
create table test_logins (
    id int(11) NOT NULL AUTO_INCREMENT,
    testid varchar(56) collate utf8_unicode_ci,
    login_ok INT DEFAULT 0,
    ok_bots varchar(2048),
    failed_bots varchar(2048),
    login_failed INT DEFAULT 0,
    remarks varchar(1024),

    PRIMARY KEY (id, testid),
    UNIQUE KEY id (id, testid)

    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;



--- alter-statements after 0.2

alter table test_results add checked_time int DEFAULT 0;
