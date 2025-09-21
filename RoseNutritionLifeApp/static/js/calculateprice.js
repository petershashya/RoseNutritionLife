// calculatePrice.js


// Function to calculate the total price
function calculatePrice() {
    var errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(function (element) {
      element.remove();
    });

// Get selected values from the form
var quality = document.getElementById('quality').value;

var structure = document.getElementById('structure').value;
var floors = document.getElementById('floors').value;
var totalArea = document.getElementById('totalarea').value;
var constructType = document.getElementById('consturcttype').value;
var location = document.getElementById('location').value;
var bedrooms = document.getElementById('bedrooms').value;
var bathrooms = document.getElementById('bathrooms').value;
var constructionPeriod = document.getElementById('construction_period').value;

var isValid = true;

  if (quality === 'null') {
    displayErrorMessage('quality', 'Please select quality of construction.');
    isValid = false;
  }
  if(totalArea === 'null'){
    displayErrorMessage('totalArea', 'Please enter Total Area.');
    isValid = false;
  }

  if (structure === 'Normal distribution ') {
    displayErrorMessage('structure', 'Please select type of structure.');
    isValid = false;
  }

  if (consturcttype === '') {
    displayErrorMessage('consturcttype', 'Please select type of construction materials.');
    isValid = false;
  }

  if (location === 'Normal distribution ') {
    displayErrorMessage('location', 'Please select location of the house.');
    isValid = false;
  }

  if (bedrooms === '') {
    displayErrorMessage('bedrooms', 'Please enter number of bedrooms.');
    isValid = false;
  }

  if (bathrooms === '') {
    displayErrorMessage('bathrooms', 'Please enter number of bathrooms.');
    isValid = false;
  }

  if (construction_period === '') {
    displayErrorMessage('construction_period', 'Please enter construction period.');
    isValid = false;
  }

  // If any input is invalid, stop further processing
  if (!isValid) {
    return;
  }



// Generate random numbers for calculation
var basePrice = Math.floor(Math.random() * 10000) + 10000; // Example base price between 1000 and 2000
var qualityMultiplier = 1; // Default multiplier
if (quality === 'basic') {
    qualityMultiplier = 0.8; // Adjust the multiplier based on quality selection
} else if (quality === 'standard') {
    qualityMultiplier = 1; // You can set different multipliers for different qualities
} else if (quality === 'luxury') {
    qualityMultiplier = 1.2;
}


var materialPrice = 0;
if (constructType === 'brick') {
    materialPrice = 200000; // Example price for brick construction
} else if (constructType === 'wood') {
    materialPrice = 150000; // Example price for wood construction
} else if (constructType === 'mixer') {
    materialPrice = 250000; // Example price for mixer construction
} else if (constructType === 'concrete') {
    materialPrice = 180000; // Example price for concrete construction
}

var structurePrice = 0;
if (structure === 'apartment') {
    structurePrice = 500000; // Example price for an apartment building
} else if (structure === 'single_family') {
    structurePrice = 800000; // Example price for a single-family house
}

// Calculate price based on location
var locationMultiplier = 1; // Default multiplier for location
if (location === 'mbeya') {
    locationMultiplier = 0.9; // Example multiplier for Mbeya location
} else if (location === 'dar') {
    locationMultiplier = 1.1; // Example multiplier for Dar location
} else if (location === 'dodoma') {
    locationMultiplier = 1.05; // Example multiplier for Dodoma location
}

 // Calculate price based on construction period
 var periodMultiplier = 1; // Default multiplier for construction period
 if (constructionPeriod >= 6 && constructionPeriod <= 12) {
     periodMultiplier = 0.9; // Example multiplier for 6-12 months construction period
 } else if (constructionPeriod > 12) {
     periodMultiplier = 0.8; // Example multiplier for more than 12 months construction period
 }

// Calculate price based on number of bedrooms and bathrooms
var roomPrice = parseInt(bedrooms) * 100000; // Example price per bedroom
roomPrice += parseInt(bathrooms) * 80000; // Example price per bathroom


// Perform calculations
var totalPrice = basePrice * qualityMultiplier;
totalPrice += parseInt(floors) * 50000; // Example cost per floor
totalPrice += parseInt(totalArea) * 20; // Example cost per square meter
totalPrice += structurePrice; // Add the price based on the structure types
totalPrice *= locationMultiplier; // Apply location multiplier to the total price
totalPrice += roomPrice; // Add the price based on number of bedrooms and bathrooms
totalPrice *= periodMultiplier; // Apply period multiplier to the total price

// Display the calculated price
('Estimated Price: $' + totalPrice.toFixed(2)); // Display the price as a formatted string


var priceContainer = document.getElementById('priceContainer');
priceContainer.innerHTML = '<p>Success! Your estimated price is: Tsh ' + totalPrice.toFixed(2) + '</p>';
  // setTimeout(function() {
  //   document.getElementById('successPopup').style.display = 'none';
  //   // You can add additional actions here after the popup disappears, if needed
  // }, 2000); // 2000 milliseconds = 2 seconds


 
}
function displayErrorMessage(inputId, message) {
    var inputElement = document.getElementById(inputId);
    var errorMessageElement = document.createElement('div');
    errorMessageElement.classList.add('error-message');
    errorMessageElement.textContent = message;
    errorMessageElement.style.color = 'red';
    inputElement.parentNode.appendChild(errorMessageElement);
  }
  