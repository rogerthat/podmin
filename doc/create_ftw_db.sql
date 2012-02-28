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
    
-- status: 0 -> UNKNOWN 1-> OK 2 -> WARNING 3 -> CRITICAL
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
