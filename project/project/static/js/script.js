document.getElementById('all').addEventListener('change', function() {
  var checkboxes = document.querySelectorAll('.rights input[type="checkbox"]');
  checkboxes.forEach(function(checkbox) {
    checkbox.checked = this.checked;
  }.bind(this));
});

