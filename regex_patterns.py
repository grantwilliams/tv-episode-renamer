PATTERNS = [
    # Sample.Show.S01E01
    r'''
    (?ix)                           # Ignore case (i), and use verbose regex (x)
    (?:s|season)?
    (\d{{1,{0}}})                   # Season number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|\-|e|ep|episode|x|^      # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    ''',

    # Sample.Show.S01E01E02
    r'''
    (?ix)                           # Ignore case (i), and use verbose regex (x)
    (?:s|season)?
    (\d{{1,{0}}})                   # Season number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|e|ep|episode|x|^         # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|\-|e|ep|episode|x|^      # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    ''',

    # Sample.Show S01E01E02E03 & Sample.Show 1x01 1x02 1x03
    r'''
    (?ix)                           # Ignore case (i), and use verbose regex (x)
    (?:s|season)?
    (\d{{1,{0}}})                   # Season number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|e|ep|episode|x|^         # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|\-|e|ep|episode|x|^      # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    \s*                             # 0-or-more whitespaces
    (?:                             # Non-grouping pattern
        \.|\-|e|ep|episode|x|^      # e or x or episode or start of a line
        )?                          # End non-grouping pattern
    \s*                             # 0-or-more whitespaces
    (\d+)                           # Episode number (Captured)
    '''
]
