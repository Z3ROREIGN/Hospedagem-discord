const { exec } = require('child_process');

module.exports = (req, res) => {
  exec('python3 main.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Erro ao iniciar o bot: ${error.message}`);
      return res.status(500).json({ error: error.message });
    }

    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }

    console.log(`stdout: ${stdout}`);
    res.status(200).json({ message: 'Bot iniciado (temporariamente).' });
  });
};
