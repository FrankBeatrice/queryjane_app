// CSS
import './../sass/layout/new_layout.scss';

// Images
import './../img/brand.svg';
import './../img/landing_page/augusta-king-transparent.png';
import './../img/brand-authenticated.svg';

// Js dependencies
import 'bootstrap';
import 'typeahead.js/dist/typeahead.jquery.min.js';
import 'jquery-validation';
import 'jquery-validation/dist/additional-methods.js';
import 'jquery-confirm/js/jquery-confirm.js';
import Bloodhound from 'typeahead.js/dist/bloodhound.min.js';
window.Bloodhound = Bloodhound;
import Quill from 'quill';
window.Quill = Quill;
import bootstrapSwitch from 'bootstrap-switch';
// TODO: Solve rateyo dependencie
import './vendor/jquery.rateyo.js';

// Utilities
import './utils/mediaQueryDetector';

// Global variables
import './globalVariables';

// Place
import './place/get_location.js';
import './place/show_position.js';

// Main
import './new_main';

// Navbar
import './navbar';
