# Skill: Modern Perl Development Patterns

## When to Use
- Writing new Perl code or modules
- Reviewing Perl code for idiom compliance
- Refactoring legacy Perl to modern standards
- Designing Perl module architecture
- Migrating pre-5.36 code to modern Perl

## Policy
Level: ALLOW

## Instructions
## How It Works

Apply these patterns as a bias toward modern Perl 5.36+ defaults: signatures, explicit modules, focused error handling, and testable boundaries. The examples below are meant to be copied as starting points, then tightened for the actual app, dependency stack, and deployment model in front of you.

## Core Principles

### 1. Use `v5.36` Pragma

A single `use v5.36` replaces the old boilerplate and enables strict, warnings, and subroutine signatures.

```perl
# Good: Modern preamble
use v5.36;

sub greet($name) {
    say "Hello, $name!";
}

# Bad: Legacy boilerplate
use strict;
use warnings;
use feature 'say', 'signatures';
no warnings 'experimental::signatures';

sub greet {
    my ($name) = @_;
    say "Hello, $name!";
}
```

### 2. Subroutine Signatures

Use signatures for clarity and automatic arity checking.

```perl
use v5.36;

# Good: Signatures with defaults
sub connect_db($host, $port = 5432, $timeout = 30) {
    # $host is required, others have defaults
    return DBI->connect("dbi:Pg:host=$host;port=$port", undef, undef, {
        RaiseError => 1,
        PrintError => 0,
    });
}

# Good: Slurpy parameter for variable args
sub log_message($level, @details) {
    say "[$level] " . join(' ', @details);
}

# Bad: Manual argument unpacking
sub connect_db {
    my ($host, $port, $timeout) = @_;
    $port    //= 5432;
    $timeout //= 30;
    # ...
}
```

### 3. Context Sensitivity

Understand scalar vs list context — a core Perl concept.

```perl
use v5.36;

my @items = (1, 2, 3, 4, 5);

my @copy  = @items;            # List context: all elements
my $count = @items;            # Scalar context: count (5)
say "Items: " . scalar @items; # Force scalar context
```

### 4. Postfix Dereferencing

Use postfix dereference syntax for readability with nested structures.

```perl
use v5.36;

my $data = {
    users => [
        { name => 'Alice', roles => ['admin', 'user'] },
        { name => 'Bob',   roles => ['user'] },
    ],
};

# Good: Postfix dereferencing
my @users = $data->{users}->@*;
my @roles = $data->{users}[0]{roles}->@*;
my %first = $data->{users}[0]->%*;

# Bad: Circumfix dereferencing (harder to read in chains)
my @users = @{ $data->{users} };
my @roles = @{ $data->{users}[0]{roles} };
```

### 5. The `isa` Operator (5.32+)

Infix type-check — replaces `blessed($o) && $o->isa('X')`.

```perl
use v5.36;
if ($obj isa 'My::Class') { $obj->do_something }
```

## Error Handling

### eval/die Pattern

```perl
use v5.36;

sub parse_config($path) {
    my $content = eval { path($path)->slurp_utf8 };
    die "Config error: $@" if $@;
    return decode_json($content);
}
```

### Try::Tiny (Reliable Exception Handling)

```perl
use v5.36;
use Try::Tiny;

sub fetch_user($id) {
    my $user = try {
        $db->resultset('User')->find($id)
            // die "User $id not found\n";
    }
    catch {
        warn "Failed to fetch user $id: $_";
        undef;
    };
    return $user;
}
```

### Native try/catch (5.40+)

```perl
use

(Content truncated for registry. See original skill for full details.)

## Constraints
- Follow the instructions above carefully.
- Report any errors or limitations clearly to the user.
- Do not perform actions outside the scope of this skill.

## Examples
User: "Help me with modern perl development patterns"
Agent: [follows the skill instructions to complete the task]
