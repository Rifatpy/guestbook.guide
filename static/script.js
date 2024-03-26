function showOption(optionId) {
  // Hide all option contents
  var optionContents = document.querySelectorAll('.option-content');
  optionContents.forEach(function(content) {
    content.classList.remove('active');
  });

  // Show the selected option content
  var selectedOption = document.getElementById(optionId);
  selectedOption.classList.add('active');
}