var $ = require('jquery');
 window.jQuery = $;
window.$ = $;
require('bootstrap');
require('typeahead.js/dist/typeahead.jquery.min.js');
var Bloodhound = require('typeahead.js/dist/bloodhound.min.js');
window.Bloodhound = Bloodhound;
require('jquery-validation');
require('jquery-validation/dist/additional-methods.js');
require('jquery-confirm');
var Quill = require('quill');
var bootstrapSwitch = require('bootstrap-switch');

// Utilities
require('./utilities/mediaQueryDetector');

// Global variables
require('./globalVariables');

// Main
require('./main');
