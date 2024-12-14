import tkinter as tk
from tkinter import ttk, messagebox
import modules.contact_remote as contact_remote
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Release Downloader")
        self.root.geometry("800x600")

        self.source_label = tk.Label(root, text="Select Source:")
        self.source_label.pack()

        self.source_var = tk.StringVar()
        self.source_dropdown = ttk.Combobox(root, textvariable=self.source_var)
        self.source_dropdown['values'] = ('GitHub', 'GitLab')
        self.source_dropdown.pack()

        self.repo_label = tk.Label(root, text="Repository (owner/repo):")
        self.repo_label.pack()

        self.repo_entry = tk.Entry(root)
        self.repo_entry.pack()

        self.fetch_button = tk.Button(
            root, text="Fetch Releases", command=self.fetch_releases)
        self.fetch_button.pack()

        self.release_label = tk.Label(root, text="Select Release:")
        self.release_label.pack()

        self.release_var = tk.StringVar()
        self.release_dropdown = ttk.Combobox(root, textvariable=self.release_var)
        self.release_dropdown.pack()

        self.artifact_label = tk.Label(root, text="Select Artifact:")
        self.artifact_label.pack()

        self.artifact_var = tk.StringVar()
        self.artifact_dropdown = ttk.Combobox(root, textvariable=self.artifact_var)
        self.artifact_dropdown.pack()

        self.download_button = tk.Button(
            root, text="Download", command=self.download_artifact)
        self.download_button.pack()

    def fetch_releases(self):
        source = self.source_var.get()
        repo = self.repo_entry.get()
        if source and repo:
            try:
                releases = contact_remote.fetch_releases(source, repo)
                if releases:
                    self.release_dropdown['values'] = releases
                    self.release_dropdown.bind("<<ComboboxSelected>>", self.fetch_artifacts)
                else:
                    messagebox.showerror("Error", "No releases found.")
                    logging.error(f"No releases found for {repo} on {source}.")
            except Exception as e:
                messagebox.showerror("Error", "Failed to fetch releases.")
                logging.error(f"Failed to fetch releases for {repo} on {source}: {e}")
        else:
            messagebox.showerror("Error", "Please select a source and enter a repository.")
            logging.error("Source or repository not provided.")

    def fetch_artifacts(self, event):
        source = self.source_var.get()
        repo = self.repo_entry.get()
        release = self.release_var.get()
        if source and repo and release:
            try:
                artifacts = contact_remote.fetch_artifacts(source, repo, release)
                if artifacts:
                    self.artifact_dropdown['values'] = artifacts
                else:
                    messagebox.showerror("Error", "No artifacts found.")
                    logging.error(f"No artifacts found for release {release} in {repo} on {source}.")
            except Exception as e:
                messagebox.showerror("Error", "Failed to fetch artifacts.")
                logging.error(f"Failed to fetch artifacts for release {release} in {repo} on {source}: {e}")
        else:
            messagebox.showerror("Error", "Please select a source, repository, and release.")
            logging.error("Source, repository, or release not provided.")

    def download_artifact(self):
        source = self.source_var.get()
        repo = self.repo_entry.get()
        artifact = self.artifact_var.get()
        if source and repo and artifact:
            try:
                success = contact_remote.download_artifact(source, repo, artifact)
                if success:
                    messagebox.showinfo("Success", "Artifact downloaded successfully.")
                else:
                    messagebox.showerror("Error", "Failed to download artifact.")
                    logging.error(f"Failed to download artifact {artifact} from {repo} on {source}.")
            except Exception as e:
                messagebox.showerror("Error", "Failed to download artifact.")
                logging.error(f"Failed to download artifact {artifact} from {repo} on {source}: {e}")
        else:
            messagebox.showerror("Error", "Please select a source, repository, and artifact.")
            logging.error("Source, repository, or artifact not provided.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
