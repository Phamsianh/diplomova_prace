CREATE TABLE public."GROUP" (
    id bigserial NOT NULL,
    name text,
    address text,
    phone int,
    PRIMARY KEY (id)
);

CREATE TABLE public."USER" (
    id bigserial NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    first_name text,
    last_name text,
    role_id bigint,
    group_id bigint,
    password text,
    email text,
    phone int,
    public_key text,
    PRIMARY KEY (id),
    FOREIGN KEY (group_id) REFERENCES public."GROUP"(id)
);

CREATE TABLE public."FORM STRUCTURE" (
    id bigserial NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    user_id bigint,
    name text,
    structure json,
    admin_digital_signature text,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES public."USER"(id)
);

CREATE TABLE public."ROLE" (
    id bigserial NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    name text,
    role_id bigint,
    PRIMARY KEY (id)
);

CREATE TABLE public."USER_ROLE" (
    id bigserial NOT NULL,
    user_id bigint,
    role_id bigint,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES public."USER"(id),
    FOREIGN KEY (role_id) REFERENCES public."ROLE"(id)
);

CREATE TABLE public."BLOCKCHAIN" (
    id bigserial NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    transaction json,
    current_hash text,
    previous_hash text,
    PRIMARY KEY (id)
);