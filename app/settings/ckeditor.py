CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'main': {
        'width': '100%',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Maximize', 'ShowBlocks', 'Undo', 'Redo', 'Paste', 'PasteText'],
            ['Format', 'FontSize', 'Bold', 'Italic', 'Underline', 'Strike'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Image', 'Iframe', 'HorizontalRule', 'SpecialChar', 'CodeSnippet'],
            ['Link', 'Unlink', 'Anchor'],
            ['RemoveFormat', 'Source']
        ],
        'allowedContent': True,
        'extraPlugins': ','.join(['codesnippet']),
        'codeSnippet_theme': 'sunburst',
        'codeSnippet_languages': {
            'apache': 'Apache',
            'bash': 'Bash',
            'coffeescript': 'CoffeeScript',
            'cpp': 'C++',
            'cs': 'C#',
            'css': 'CSS',
            'diff': 'Diff',
            'html': 'HTML',
            'http': 'HTTP',
            'ini': 'INI',
            'java': 'Java',
            'javascript': 'JavaScript',
            'json': 'JSON',
            'makefile': 'Makefile',
            'markdown': 'Markdown',
            'nginx': 'Nginx',
            'objectivec': 'Objective-C',
            'perl': 'Perl',
            'php': 'PHP',
            'python': 'Python',
            'ruby': 'Ruby',
            'sql': 'SQL',
            'shell': 'Shell',
            'vbscript': 'VBScript',
            'xml': 'XML'
        }
    },
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
}
