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
window.Quill = Quill;
var bootstrapSwitch = require('bootstrap-switch');
window.bootstrapSwitch = bootstrapSwitch;
require('rateyo/min/jquery.rateyo.min.js');

// Utilities
require('./utilities/mediaQueryDetector');

// Global variables
require('./globalVariables');

// Main
require('./main');
