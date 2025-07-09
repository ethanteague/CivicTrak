/**
 * @file
 * Global utilities.
 *
 */
((Drupal) => {
  Drupal.behaviors.gov = {
    attach: function(context, settings) {
      const yearElement = document.getElementById("year");
      if (yearElement) {
        yearElement.textContent = new Date().getFullYear().toString();
      }
    }
  };

})(Drupal);
