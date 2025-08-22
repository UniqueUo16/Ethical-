// Text Processor JavaScript Functions

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Set up tool navigation
    setupToolNavigation();
    
    // Set up real-time text counting
    setupTextCounters();
    
    // Initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});

// Tool Navigation Setup
function setupToolNavigation() {
    const navLinks = document.querySelectorAll('[data-tool]');
    const toolSections = document.querySelectorAll('.tool-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Hide all tool sections
            toolSections.forEach(section => section.classList.add('d-none'));
            
            // Show selected tool section
            const toolId = this.getAttribute('data-tool');
            const targetSection = document.getElementById(toolId);
            if (targetSection) {
                targetSection.classList.remove('d-none');
            }
        });
    });
}

// Setup real-time text counters
function setupTextCounters() {
    // Case converter character count
    const caseInput = document.getElementById('case-input');
    if (caseInput) {
        caseInput.addEventListener('input', function() {
            document.getElementById('case-char-count').textContent = this.value.length;
        });
    }
    
    // Text counter real-time updates
    const counterInput = document.getElementById('counter-input');
    if (counterInput) {
        counterInput.addEventListener('input', function() {
            countText();
        });
    }
}

// Case Conversion Functions
function convertCase(caseType) {
    const input = document.getElementById('case-input').value;
    const output = document.getElementById('case-output');
    
    if (!input.trim()) {
        showToast('Please enter some text to convert', 'warning');
        return;
    }
    
    const data = {
        text: input,
        case_type: caseType
    };
    
    fetch('/api/convert-case', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
        } else {
            output.value = data.result;
            showToast('Text converted successfully!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during conversion', 'danger');
    });
}

// Text Counting Function
function countText() {
    const input = document.getElementById('counter-input').value;
    
    const data = {
        text: input
    };
    
    fetch('/api/count-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            document.getElementById('stat-characters').textContent = data.characters;
            document.getElementById('stat-characters-no-spaces').textContent = data.characters_no_spaces;
            document.getElementById('stat-words').textContent = data.words;
            document.getElementById('stat-sentences').textContent = data.sentences;
            document.getElementById('stat-paragraphs').textContent = data.paragraphs;
            document.getElementById('stat-reading-time').textContent = data.reading_time;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Find and Replace Function
function findReplace() {
    const input = document.getElementById('fr-input').value;
    const findText = document.getElementById('find-text').value;
    const replaceText = document.getElementById('replace-text').value;
    const caseSensitive = document.getElementById('case-sensitive').checked;
    const useRegex = document.getElementById('use-regex').checked;
    const output = document.getElementById('fr-output');
    const status = document.getElementById('replace-status');
    
    if (!input.trim()) {
        showToast('Please enter some text to process', 'warning');
        return;
    }
    
    if (!findText) {
        showToast('Please enter text to find', 'warning');
        return;
    }
    
    const data = {
        text: input,
        find: findText,
        replace: replaceText,
        case_sensitive: caseSensitive,
        use_regex: useRegex
    };
    
    fetch('/api/find-replace', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
            status.textContent = '';
        } else {
            output.value = data.result;
            status.textContent = `${data.replacements} replacement(s) made`;
            showToast('Find and replace completed!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during find and replace', 'danger');
    });
}

// Text Cleaning Function
function cleanText(cleanType) {
    const input = document.getElementById('clean-input').value;
    const output = document.getElementById('clean-output');
    
    if (!input.trim()) {
        showToast('Please enter some text to clean', 'warning');
        return;
    }
    
    const data = {
        text: input,
        clean_type: cleanType
    };
    
    fetch('/api/clean-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
        } else {
            output.value = data.result;
            showToast('Text cleaned successfully!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during text cleaning', 'danger');
    });
}

// Text Formatting Function
function formatText(formatType) {
    const input = document.getElementById('format-input').value;
    const output = document.getElementById('format-output');
    
    if (!input.trim()) {
        showToast('Please enter some text to format', 'warning');
        return;
    }
    
    const data = {
        text: input,
        format_type: formatType
    };
    
    fetch('/api/format-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
        } else {
            output.value = data.result;
            showToast('Text formatted successfully!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during text formatting', 'danger');
    });
}

// SEO Analysis Function
function analyzeSEO() {
    const input = document.getElementById('seo-input').value;
    const keyword = document.getElementById('seo-keyword').value;
    const resultsDiv = document.getElementById('seo-results');
    
    if (!input.trim()) {
        showToast('Please enter some text to analyze', 'warning');
        return;
    }
    
    const data = {
        text: input,
        keyword: keyword
    };
    
    fetch('/api/seo-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
        } else {
            resultsDiv.innerHTML = `
                <div class="stat-item">
                    <strong>Keyword Density:</strong> ${data.keyword_density}%
                </div>
                <div class="stat-item">
                    <strong>Readability Score:</strong> ${data.readability_score}/100
                </div>
                <div class="stat-item">
                    <strong>Readability Level:</strong> ${data.readability_level}
                </div>
                <div class="stat-item">
                    <strong>Avg. Sentence Length:</strong> ${data.avg_sentence_length} words
                </div>
                <div class="stat-item">
                    <strong>Avg. Syllables per Word:</strong> ${data.avg_syllables_per_word}
                </div>
            `;
            showToast('SEO analysis completed!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during SEO analysis', 'danger');
    });
}

// Text Comparison Function
function compareTexts() {
    const text1 = document.getElementById('compare-text1').value;
    const text2 = document.getElementById('compare-text2').value;
    const resultsDiv = document.getElementById('comparison-results');
    
    if (!text1.trim() || !text2.trim()) {
        showToast('Please enter text in both fields to compare', 'warning');
        return;
    }
    
    const data = {
        text1: text1,
        text2: text2
    };
    
    fetch('/api/compare-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, 'danger');
        } else {
            resultsDiv.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6>Text 1 Statistics</h6>
                        <div class="stat-item">Characters: ${data.text1_stats.characters}</div>
                        <div class="stat-item">Words: ${data.text1_stats.words}</div>
                    </div>
                    <div class="col-md-6">
                        <h6>Text 2 Statistics</h6>
                        <div class="stat-item">Characters: ${data.text2_stats.characters}</div>
                        <div class="stat-item">Words: ${data.text2_stats.words}</div>
                    </div>
                </div>
                <hr>
                <div class="stat-item">
                    <strong>Character Difference:</strong> ${data.char_difference > 0 ? '+' : ''}${data.char_difference}
                </div>
                <div class="stat-item">
                    <strong>Word Difference:</strong> ${data.word_difference > 0 ? '+' : ''}${data.word_difference}
                </div>
                <div class="stat-item">
                    <strong>Similarity:</strong> ${data.similarity_percentage}%
                </div>
            `;
            showToast('Text comparison completed!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred during text comparison', 'danger');
    });
}

// Copy to Clipboard Function
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    if (!element.value.trim()) {
        showToast('Nothing to copy', 'warning');
        return;
    }
    
    element.select();
    element.setSelectionRange(0, 99999); // For mobile devices
    
    try {
        document.execCommand('copy');
        showToast('Copied to clipboard!', 'success');
    } catch (err) {
        // Fallback for modern browsers
        navigator.clipboard.writeText(element.value).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy to clipboard', 'danger');
        });
    }
}

// Export Text Function
function exportText(elementId, filename) {
    const element = document.getElementById(elementId);
    if (!element.value.trim()) {
        showToast('Nothing to export', 'warning');
        return;
    }
    
    const data = {
        text: element.value,
        filename: filename
    };
    
    fetch('/api/export-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Export failed');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showToast('File exported successfully!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Failed to export file', 'danger');
    });
}

// Toast Notification Function
function showToast(message, type = 'info') {
    // Remove any existing toasts
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 3000);
}
