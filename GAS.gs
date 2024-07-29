function doGet(e) {
  // Hardcoded values
  var emailAddress = "teohkl-pm21@student.tarc.edu.my";
  var subject = "New Upload Notification";
  var message = "A new file has been uploaded to the resume application.\n\n" +
                "Please check the application for details.";

  // Send email
  MailApp.sendEmail({
    to: emailAddress,
    subject: subject,
    body: message
  });

  return ContentService.createTextOutput("Notification sent");
}