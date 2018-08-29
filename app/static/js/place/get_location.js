function getLocation() {
  if (navigator.geolocation) {
      $('.QjaneShareGPSloading').show();
      $('.QjaneShareGPSfigure').hide();
      navigator.geolocation.getCurrentPosition(function(position) {
          showPosition(position);
      }, function() {
          $('.QjaneShareGPSloading').hide();
          $('.QjaneShareGPSfigure').show();
      });
  } else {
      alert("Geolocation is not supported by this browser.");
  }
}

window.getLocation = getLocation;
