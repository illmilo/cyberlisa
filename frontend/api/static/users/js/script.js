function toggleCheckList(element) {
  // Toggle visibility
  element.classList.toggle('visible');
  
  // Find the anchor element
  const anchor = element.querySelector('.anchor');
  
  // Update the arrow rotation
  if (element.classList.contains('visible')) {
    anchor.style.setProperty('--arrow-rotation', '45deg');
    anchor.style.setProperty('--arrow-position', '40%');
  } else {
    anchor.style.setProperty('--arrow-rotation', '-135deg');
    anchor.style.setProperty('--arrow-position', '10%');
  }
}