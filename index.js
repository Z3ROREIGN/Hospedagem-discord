const { exec } = require('child_process');

exports.handler = async (event, context) => {
  // Start the Discord bots
  exec('python main.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error starting Discord bots: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Error starting Discord bots: ${stderr}`);
      return;
    }
    console.log('Discord bots started successfully.');
  });

  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Discord bots started successfully.' }),
  };
};
