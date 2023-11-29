
# Config File Formats

Config fix to use our application
## TXT Format
```txt
Configuration:
    General:
        Username: [USERNAME]
        Email: [EMAIL_ADDRESS]
        Password: [PASSWORD]
        MailServer: [MAIL_SERVER_IP]
        SMTP: [SMTP_PORT]
        POP3: [POP3_PORT]
        AutoLoad: [AUTOLOAD_INTERVAL]

    Filters:
        Filter:
            ApplyTo: From
            Keywords:
                - Keyword: [EMAIL_KEYWORDS_FOR_FROM_FILTER]
            Folder: [FOLDER_NAME_FOR_FROM_FILTER]

        Filter:
            ApplyTo: Subject
            Keywords:
                - Keyword: [KEYWORDS_FOR_SUBJECT_FILTER]
            Folder: [FOLDER_NAME_FOR_SUBJECT_FILTER]

        Filter:
            ApplyTo: Content
            Keywords:
                - Keyword: [KEYWORDS_FOR_CONTENT_FILTER]
            Folder: [FOLDER_NAME_FOR_CONTENT_FILTER]

        Filter:
            ApplyTo:
                - Type: Subject
                - Type: Content
            Keywords:
                - Keyword: [KEYWORDS_FOR_SUBJECT_AND_CONTENT_FILTER]
            Folder: [FOLDER_NAME_FOR_SUBJECT_AND_CONTENT_FILTER]

```

## XML Format
```xml
<Configuration>
    <General>
        <Username>[USERNAME]</Username>
        <Email>[EMAIL_ADDRESS]</Email>
        <Password>[PASSWORD]</Password>
        <MailServer>[MAIL_SERVER_IP]</MailServer>
        <SMTP>[SMTP_PORT]</SMTP>
        <POP3>[POP3_PORT]</POP3>
        <AutoLoad>[AUTOLOAD_INTERVAL]</AutoLoad>
    </General>
    <Filters>
        <Filter>
            <ApplyTo>From</ApplyTo>
            <Keywords>
                <Keyword>[EMAIL_KEYWORDS_FOR_FROM_FILTER]</Keyword>
            </Keywords>
            <Folder>[FOLDER_NAME_FOR_FROM_FILTER]</Folder>
        </Filter>
        <Filter>
            <ApplyTo>Subject</ApplyTo>
            <Keywords>
                <Keyword>[KEYWORDS_FOR_SUBJECT_FILTER]</Keyword>
            </Keywords>
            <Folder>[FOLDER_NAME_FOR_SUBJECT_FILTER]</Folder>
        </Filter>
        <Filter>
            <ApplyTo>Content</ApplyTo>
            <Keywords>
                <Keyword>[KEYWORDS_FOR_CONTENT_FILTER]</Keyword>
            </Keywords>
            <Folder>[FOLDER_NAME_FOR_CONTENT_FILTER]</Folder>
        </Filter>
        <Filter>
            <ApplyTo>
                <Type>Subject</Type>
                <Type>Content</Type>
            </ApplyTo>
            <Keywords>
                <Keyword>[KEYWORDS_FOR_SUBJECT_AND_CONTENT_FILTER]</Keyword>
            </Keywords>
            <Folder>[FOLDER_NAME_FOR_SUBJECT_AND_CONTENT_FILTER]</Folder>
        </Filter>
    </Filters>
</Configuration>
```

## JSON Format

```json
{
  "general": {
    "Username": "<USERNAME>",
    "Email": "<EMAIL_ADDRESS>",
    "Password": "<PASSWORD>",
    "MailServer": "<MAIL_SERVER_IP>",
    "SMTP": "<SMTP_PORT>",
    "POP3": "<POP3_PORT>",
    "AutoLoad": "<AUTOLOAD_INTERVAL>"
  },
  "filters": [
    {
      "applyTo": ["From"],
      "keywords": ["<EMAIL_KEYWORDS_FOR_FROM_FILTER>"],
      "folder": "<FOLDER_NAME_FOR_FROM_FILTER>"
    },
    {
      "applyTo": ["Subject"],
      "keywords": ["<KEYWORDS_FOR_SUBJECT_FILTER>"],
      "folder": "<FOLDER_NAME_FOR_SUBJECT_FILTER>"
    },
    {
      "applyTo": ["Content"],
      "keywords": ["<KEYWORDS_FOR_CONTENT_FILTER>"],
      "folder": "<FOLDER_NAME_FOR_CONTENT_FILTER>"
    },
    {
      "applyTo": ["Subject", "Content"],
      "keywords": ["<KEYWORDS_FOR_SUBJECT_AND_CONTENT_FILTER>"],
      "folder": "<FOLDER_NAME_FOR_SUBJECT_AND_CONTENT_FILTER>"
    }
  ]
}
```

