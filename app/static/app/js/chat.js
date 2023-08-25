
$(document).ready(function() {
    const messageInput = $('#message-input');
    const sendButton = $('#send-button');
    const chatMessages = $('#chat-messages');
    const toggler = $('.chatbot-toggler');
    const chatSection = $('#chat-section');

    const responses = {
        'hi': 'Hello there!',
        'hello': 'Hello there!',
        'how are you': 'I am just a bot, but I am doing fine!',
        'name': "I'm just a chatbot, so I don't have a name.",
        'who are you': "I'm a simple chatbot designed to assist you.",
        'what products do you offer?': 'We offer a wide range of products, including electronics, clothing, home goods, and more.',
        'how do I place an order?': 'To place an order, simply browse our products, add items to your cart, and proceed to checkout.',
        'can I track my order?': 'Yes, you can track your order by logging into your account and viewing your order history.',
        'how long does shipping take?': 'Shipping times vary depending on your location and the selected shipping method. You can find estimated delivery times during checkout.',
        'do you offer international shipping?': 'Yes, we offer international shipping to many countries. You can select your country during checkout to see if it\'s available.',
        'what payment methods do you accept?': 'We accept a variety of payment methods, including credit/debit cards and online payment platforms like PayPal.',
        'how do I return an item?': 'If you want to return an item, you can initiate the return process through your account\'s order history.',
        'is there a loyalty program?': 'Yes, we have a loyalty program that offers rewards for repeat customers.',
        'can I cancel an order?': 'You can cancel an order within a specified timeframe after placing it. Check your order history for more details.',
        'are there discounts available?': 'We offer discounts and promotions periodically. Keep an eye out for announcements on our website.',
        'how can I contact customer support?': 'You can reach our customer support team through the contact information provided on our website.',
        'is my personal information secure?': 'Yes, we prioritize the security of your personal information and use encryption to protect your data.',
        'can I change my shipping address?': 'You can update your shipping address in your account settings or during the checkout process.',
        'what should I do if I receive a damaged item?': 'If you receive a damaged item, please contact our customer support immediately for assistance.',
        'do you offer gift wrapping?': 'Yes, we offer gift wrapping services for select items during the checkout process.',
        'how do I create an account?': 'You can create an account by clicking the \'Sign Up\' button on our website and providing the required information.',
        'can I save items for later?': 'Yes, you can add items to your wishlist to save them for later.',
        'what is the return policy?': 'Our return policy allows you to return items within a specified timeframe for a refund or exchange. Check our website for details.',
        'how can I check my order status?': 'You can check your order status by logging into your account and viewing your order history.',
        'is there a mobile app available?': 'Yes, we have a mobile app available for download on both iOS and Android platforms.',
        'do you offer price matching?': 'Yes, we offer price matching for certain products. Please review our price matching policy on our website.',
        'can I change or cancel my order after it\'s placed?': 'Orders can be changed or canceled within a specific timeframe after being placed. Please contact our customer support for assistance.',
        'how do I apply a coupon code?': 'You can apply a coupon code during the checkout process in the designated field.',
        'what is your customer satisfaction guarantee?': 'We are committed to customer satisfaction. If you are not happy with your purchase, contact us for assistance.',
        'how can I provide feedback on my shopping experience?': 'We welcome your feedback! You can leave a review on our website or contact our customer support.',
        'do you offer expedited shipping?': 'Yes, we offer expedited shipping options for faster delivery. You can select this option during checkout.',
        'how can I unsubscribe from marketing emails?': 'You can unsubscribe from marketing emails by clicking the \'Unsubscribe\' link at the bottom of any email you receive from us.',
        'what is your price range for products?': 'Our products range in price depending on the category. You can find items within your budget by browsing our website.',
        'can I save my payment information for future purchases?': 'For security reasons, we do not store payment information. You\'ll need to enter your payment details each time you make a purchase.',
        'how do I provide feedback on a specific product?': 'You can leave a review for a specific product on its product page. Your feedback is valuable to us.',
        'what is your privacy policy?': 'Our privacy policy outlines how we collect, use, and protect your personal information. You can find it on our website.',
        'are there any ongoing sales or promotions?': 'We regularly offer sales and promotions. Visit our website\'s \'Sale\' section to view ongoing discounts.',
        'can I change my order\'s shipping method?': 'You can change the shipping method for an order within a specific timeframe after placing it. Contact our customer support for assistance.',
        'is there a size guide for clothing?': 'Yes, you can find size guides for our clothing items on their respective product pages.',
        'how do I earn loyalty rewards?': 'You can earn loyalty rewards by making purchases and accumulating points. Check your account\'s rewards section for more information.',
        'do you offer gift cards?': 'Yes, we offer gift cards that can be used to make purchases on our website.',
        'how can I change my password?': 'You can change your password by logging into your account and accessing the account settings.',
        'what is your shipping policy for heavy items?': 'Our shipping policy for heavy items may vary. Please refer to our website\'s shipping policy section for specific details.',
        'are there customer reviews for products?': 'Yes, you can find customer reviews for most of our products on their respective product pages.',
        'how can I get notified about new arrivals?': 'You can sign up for our newsletter to receive notifications about new arrivals and promotions.',
        'can I change the delivery address after placing an order?': 'Delivery addresses can be changed within a specific timeframe after placing an order. Contact our customer support for assistance.',
        'how do I redeem a gift card?': 'You can redeem a gift card by entering the gift card code during the checkout process.',
        // Add more responses here
    };
    

    const suggestions = Object.keys(responses);

    // Display suggestions as the user types
    messageInput.on('input', function() {
        const userInput = messageInput.val().toLowerCase();
        const filteredSuggestions = suggestions.filter(suggestion =>
            suggestion.includes(userInput)
        );

        const datalist = $('#suggestions');
        datalist.empty();
        filteredSuggestions.forEach(suggestion => {
            datalist.append(`<option value="${suggestion}">`);
        });
    });

    // Send message when user clicks send button
    sendButton.on('click', function() {
        const messageText = messageInput.val().trim();
        if (messageText !== '') {
            const inputMessage = createMessage(messageText, 'input-message');
            chatMessages.append(inputMessage);

            // Simulate bot response after a short delay
            setTimeout(() => {
                const responseText = responses[messageText.toLowerCase()] || "I'm sorry, I don't understand.";
                const outputMessage = createMessage(responseText, 'output-message');
                chatMessages.append(outputMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 500);

            messageInput.val('');
        }
    });

    // Create a message element
    function createMessage(text, className) {
        const messageDiv = $('<div></div>');
        messageDiv.text(text);
        messageDiv.addClass('message ' + className);
        return messageDiv;
    }

    // Toggle chat container
    toggler.on('click', function() {
        chatSection.toggleClass('show-chatcontainer');
    });
});
