(function () {
    'use strict';

    function initializeEditors() {
        if (!window.Jodit) return;

        document.querySelectorAll('textarea[name="description"], textarea[name="description_ru"]').forEach(function (textarea) {
            if (textarea.dataset.joditInitialized) return;
            textarea.dataset.joditInitialized = 'true';
            Jodit.make(textarea, {
                theme: 'dark',
                width: '100%',
                height: 360,
                minHeight: 220,
                toolbarAdaptive: false,
                buttons: [
                    'bold', 'italic', 'underline', '|',
                    'ul', 'ol', '|',
                    'paragraph', 'align', '|',
                    'link', 'hr', '|', 'undo', 'redo', 'source'
                ],
                // Images and arbitrary embedded content are intentionally excluded.
                iframe: false,
                spellcheck: true,
                uploader: { insertImageAsBase64URI: false }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeEditors);
    } else {
        initializeEditors();
    }
}());
