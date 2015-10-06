/* jshint undef: true, unused: true */
/* globals tinymce, jQuery */

"use strict";

var script = document.getElementById('protect-script');

if(script){
  var base_url = script.getAttribute('data-site-url');
  var token = script.getAttribute('data-token');

  if(jQuery){
    jQuery.ajaxSetup({
      beforeSend: function (xhr, options){
        if(!options.url){
          return;
        }
        if(options.url.indexOf('_authenticator') !== -1){
          return;
        }
        if(options.url.indexOf(base_url) === 0){
          // only urls that start with the site url
          xhr.setRequestHeader("X-CSRF-TOKEN", token);
        }
      }
    });
  }
  if(tinymce){
    tinymce.util.XHR._send = tinymce.util.XHR.send;
    tinymce.util.XHR.send = function(){
      var args = Array.prototype.slice.call(arguments);
      if(args[0]){
        var config = args[0];
        if(config.data && typeof(config.data) === 'string' &&
            config.url && config.url.indexOf(base_url) === 0){
          config.data = config.data + '&_authenticator=' + token;
        }
      }
      tinymce.util.XHR._send.apply(tinymce.util.XHR, args);
    };
  }
}