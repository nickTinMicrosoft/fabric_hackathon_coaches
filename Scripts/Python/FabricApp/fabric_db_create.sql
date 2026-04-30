

create table [users] (
    id int primary key identity(1,1),
    USERID nvarchar(50),
    REDUCTION nvarchar(255),
    LEACODE nvarchar(50),
    SCHOOLCODE nvarchar(50),
    date_refreshed datetime
)

