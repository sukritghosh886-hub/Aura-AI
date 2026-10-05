create extension if not exists pgcrypto;

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    display_name text,
    created_at timestamptz not null default now()
);

create table if not exists public.conversations (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    title text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.messages (
    id uuid primary key default gen_random_uuid(),
    conversation_id uuid not null references public.conversations(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    role text not null check (role in ('user','assistant','system')),
    content text not null,
    created_at timestamptz not null default now()
);

create table if not exists public.memories (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    memory_type text not null default 'general',
    content text not null,
    importance integer not null default 1,
    created_at timestamptz not null default now()
);

create table if not exists public.tasks (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    objective text not null,
    status text not null default 'queued'
        check (status in ('queued','planning','running','waiting','completed','failed','cancelled')),
    priority integer not null default 5,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.agent_runs (
    id uuid primary key default gen_random_uuid(),
    task_id uuid references public.tasks(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    agent_name text not null,
    status text not null default 'started',
    started_at timestamptz not null default now(),
    finished_at timestamptz
);

create table if not exists public.agent_events (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    task_id uuid references public.tasks(id) on delete cascade,
    run_id uuid references public.agent_runs(id) on delete cascade,
    event_type text not null,
    message text,
    payload jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists public.tool_executions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    task_id uuid references public.tasks(id) on delete cascade,
    tool_name text not null,
    action text not null,
    status text not null default 'requested',
    input jsonb not null default '{}'::jsonb,
    output jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists public.approvals (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    task_id uuid references public.tasks(id) on delete cascade,
    action text not null,
    risk_level text not null default 'medium',
    status text not null default 'pending'
        check (status in ('pending','approved','rejected','expired')),
    created_at timestamptz not null default now(),
    decided_at timestamptz
);

create table if not exists public.security_scans (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    target_name text not null,
    target_type text not null,
    authorization_confirmed boolean not null default false,
    status text not null default 'queued',
    risk_score integer not null default 0,
    summary text,
    findings jsonb not null default '[]'::jsonb,
    created_at timestamptz not null default now(),
    completed_at timestamptz
);

create table if not exists public.security_findings (
    id uuid primary key default gen_random_uuid(),
    scan_id uuid not null references public.security_scans(id) on delete cascade,
    severity text not null,
    category text not null,
    title text not null,
    description text not null,
    recommendation text,
    evidence jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists public.audit_logs (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete set null,
    event_type text not null,
    actor text not null default 'aura',
    action text,
    resource text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create index if not exists conversations_user_idx
on public.conversations(user_id);

create index if not exists messages_conversation_idx
on public.messages(conversation_id);

create index if not exists memories_user_idx
on public.memories(user_id);

create index if not exists tasks_user_idx
on public.tasks(user_id);

create index if not exists events_user_idx
on public.agent_events(user_id);

create index if not exists scans_user_idx
on public.security_scans(user_id);

create index if not exists findings_scan_idx
on public.security_findings(scan_id);

alter table public.profiles enable row level security;
alter table public.conversations enable row level security;
alter table public.messages enable row level security;
alter table public.memories enable row level security;
alter table public.tasks enable row level security;
alter table public.agent_runs enable row level security;
alter table public.agent_events enable row level security;
alter table public.tool_executions enable row level security;
alter table public.approvals enable row level security;
alter table public.security_scans enable row level security;
alter table public.security_findings enable row level security;
alter table public.audit_logs enable row level security;

create policy "profiles_owner"
on public.profiles
for all
to authenticated
using ((select auth.uid()) = id)
with check ((select auth.uid()) = id);

create policy "conversations_owner"
on public.conversations
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "messages_owner"
on public.messages
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "memories_owner"
on public.memories
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "tasks_owner"
on public.tasks
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "agent_runs_owner"
on public.agent_runs
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "agent_events_owner"
on public.agent_events
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "tool_executions_owner"
on public.tool_executions
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "approvals_owner"
on public.approvals
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "security_scans_owner"
on public.security_scans
for all
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);

create policy "security_findings_owner"
on public.security_findings
for select
to authenticated
using (
    exists (
        select 1
        from public.security_scans s
        where s.id = scan_id
        and s.user_id = (select auth.uid())
    )
);

create policy "audit_logs_owner"
on public.audit_logs
for select
to authenticated
using ((select auth.uid()) = user_id);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security invoker
as $$
begin
    insert into public.profiles (id, display_name)
    values (
        new.id,
        coalesce(new.raw_user_meta_data ->> 'display_name', '')
    );

    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row
execute function public.handle_new_user();