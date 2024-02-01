import * as Docker from 'dockerode';
import { Injectable } from '@nestjs/common';
import { mkdirSync } from 'fs';
import { join } from 'path';
import { v4 as uuidv4 } from 'uuid';

/**
 * This service is responsible for interacting with the Docker API.
 * It is used by the ExecutionWsGateway to start containers and send input to them.
 * Currently only a test with Python is implemented.
 */
@Injectable()
export class ExecutionWsService {
    private docker: Docker;

    // sets the docker runtime to be used (runc (default), runsc, runsc-debug)
    private runtime: string = process.env.DOCKER_RUNTIME ||
        'runc';
    //    'runsc';
    //    'runsc-debug';

    // The docker images to use for the different languages. Make sure that the images are available locally.
    private readonly pythonImage = process.env.DOCKER_IMAGE_PYTHON || 'python-interactive';

    // Map of session IDs to containers
    private sessionContainers = new Map<string, Docker.Container>();

    /**
     * Creates an instance of ExecutionWsService.
     */
    constructor() {
        // Choose the correct Docker configuration based on the environment
        const isWindows = process.platform === "win32";
        this.docker = new Docker(isWindows ? { socketPath: '//./pipe/docker_engine' } : { socketPath: '/var/run/docker.sock' });

        // Alternative configuration for Docker using TCP
        // this.docker = new Docker({ host: '127.0.0.1', port: 2375 });
    }

    /**
     * Starts an interactive python session
     * @param { Record<string, string> } files - The files of the session (filename: base64 encoded content)
     * @returns { Promise<string> } - The session ID of the started session
     */
    async startPythonSession(): Promise<string> {
        const sessionId = uuidv4();
        const tempDir = join(__dirname, 'temp', sessionId);
        mkdirSync(tempDir, { recursive: true });

        // Start Docker container
        const container = await this.startInteractiveSession(this.pythonImage, tempDir);

        // Register container
        this.registerContainer(sessionId, container);

        return sessionId; // Return the session ID to the client
    }

    /**
     * Starts an interactive session with the given image.
     * @param { string } image - The Docker image to start the session with.
     * @param { string } tempDir - The temporary directory to mount as workspace.
     * @returns { Promise<Docker.Container> } - The started container.
     */
    async startInteractiveSession(image: string, tempDir: string): Promise<Docker.Container> {
        const container = await this.docker.createContainer({
            Image: image,
            Cmd: ['node', '/commandListener/commandListener.js'],
            Tty: true,
            OpenStdin: true,
            AttachStdin: true,
            AttachStdout: true,
            AttachStderr: true,
            WorkingDir: '/commandListener',
            HostConfig: {
                Runtime: this.runtime,
            }
        });
        await container.start();
        return container;
    }

    /**
     * Signals the start of the program in the given container. The program is assumed to be called main.py.
     * @param { Docker.Container } container - The container to signal the start to.
     */
    async startProgram(container: Docker.Container): Promise<void> {
        const exec = await container.exec({
            Cmd: ['sh', '-c', 'echo "run" > /commandListener/commands.txt'],
            AttachStdin: true,
            AttachStdout: true,
            AttachStderr: true,
            Tty: true,
        });

        await exec.start({ Detach: false });
    }

    /**
     * Creates or updates the files in the given container.
     * @param { Docker.Container } container - The container to create or update the files in.
     * @param { Record<string, string> } files - The files to update.
     * @todo Check if the files are base64 encoded.
     */
    async upsertFiles(container: Docker.Container, files: Record<string, string>): Promise<void> {
        // Construct the command string with all file updates
        let commandString = '';
        for (const [filename, content] of Object.entries(files)) {
            commandString += `upsert ${filename} ${content}\n`;
        }

        // Send the command string to the container
        const exec = await container.exec({
            Cmd: ['sh', '-c', `echo "${commandString}" > /commandListener/commands.txt`],
            AttachStdin: true,
            AttachStdout: true,
            AttachStderr: true,
            Tty: true,
        });

        await exec.start({ Detach: false });
    }

    /**
     * Sends the given input to the given container.
     * @param { Docker.Container } container - The container to send the input to.
     * @param { string } input - The input to send.
     */
    async sendInput(container: Docker.Container, input: string): Promise<void> {
        const command = `input ${input}`;
        const exec = await container.exec({
            Cmd: ['sh', '-c', `echo "${command}" >> /commandListener/commands.txt`],
            AttachStdin: true,
            AttachStdout: true,
            AttachStderr: true,
            Tty: true,
        });

        await exec.start({ Detach: false });
    }

    /**
     * Sets up a listener for the output of the given container.
     * @param { Docker.Container } container - The container to listen to.
     * @param { (data: string) => void } callback - The callback to call when new output is available.
     */
    async setupContainerOutputListener(container: Docker.Container, callback: (data: string) => void): Promise<void> {
        const stream = await container.attach({
            stream: true,
            stdout: true,
            stderr: true
        });
        stream.setEncoding('utf8');
        stream.on('data', callback);
    }

    /**
     * Gets the container for the given session ID.
     * @param { string } sessionId - The session ID to get the container for.
     * @returns { Promise<Docker.Container | undefined> } - The container for the given session ID, or undefined if no container is registered.
     */
    async getContainer(sessionId: string): Promise<Docker.Container | undefined> {
        console.log(`Retrieving container for session: ${sessionId}`);
        return this.sessionContainers.get(sessionId);
    }

    /**
     * Registers the given container for the given session ID.
     * @param { string } sessionId - The session ID to register the container for.
     * @param { Docker.Container } container - The container to register.
     */
    registerContainer(sessionId: string, container: Docker.Container): void {
        this.sessionContainers.set(sessionId, container);
        console.log(`Registering container for session: ${sessionId}`);
    }
}
