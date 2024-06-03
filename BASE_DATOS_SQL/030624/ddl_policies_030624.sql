CREATE SEQUENCE public.policy_id_seq
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    START WITH 1;
    
CREATE TABLE public.policies (
    id UUID PRIMARY KEY,
    amount_insured FLOAT8 NOT NULL,
    email VARCHAR(120) NOT NULL,
    inception_date TIMESTAMP NOT NULL,
    installment_payment BOOLEAN NOT NULL,
    client_id UUID REFERENCES public.clients(id)
);