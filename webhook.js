const express = require('express');
const bodyParser = require('body-parser');
const simpleGit = require('simple-git');
const { exec } = require('child_process');

const app = express();
const git = simpleGit();

app.use(bodyParser.json());

app.post('/github-webhook', (req, res) => {
    if (req.headers['x-github-event'] === 'push') {
        console.log('Received GitHub push event');
        
        // Pull the latest code from GitHub
        git.pull('origin', 'main', (err, update) => {
            if (err) {
                console.error('Error pulling from GitHub:', err);
            } else if (update && update.summary.changes) {
                console.log('Successfully pulled new changes');
                
                // Restart the program using PM2
                exec('pm2 restart your_app_name', (error, stdout, stderr) => {
                    if (error) {
                        console.error(`Error restarting app: ${error.message}`);
                    }
                    console.log(`stdout: ${stdout}`);
                    console.error(`stderr: ${stderr}`);
                });
            }
        });
    }
    res.status(200).send('Webhook received');
});

app.listen(8000, () => console.log('Webhook listener running on port 8000'));
