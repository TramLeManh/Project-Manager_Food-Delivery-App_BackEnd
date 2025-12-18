create type user_role as enum ('USER', 'ADMIN');

alter type user_role owner to root;

create type user_role_enum as enum ('USER', 'ADMIN');

alter type user_role_enum owner to root;

create table "user"
(
    user_id       uuid,
    email         varchar(50)
        constraint unique_email
            unique,
    mobile_number varchar(15),
    address       varchar(100),
    password      varchar(100),
    created_at    timestamp,
    role          user_role_enum default 'USER'::user_role_enum not null
);

alter table "user"
    owner to root;

