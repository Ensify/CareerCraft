from app.mongo import MongoHandle
from app.utils.claude import RoadmapClaude

mongo_handle = MongoHandle()

def generate_roadmap(project, quizzes):
    # TODO
    return   [
        {
            "title": "Set up the project environment",
            "milestones": [
                {
                    "title": "Install required libraries",
                    "tasks": [
                        {
                            "task": "Install Python and required packages",
                            "description": "Install Python, TensorFlow, Flask, and any other necessary libraries for the project."
                        },
                        {
                            "task": "Set up a virtual environment",
                            "description": "Create a virtual environment to isolate the project dependencies and avoid conflicts with other projects."
                        }
                    ]
                },
                {
                    "title": "Explore the dataset",
                    "tasks": [
                        {
                            "task": "Obtain a suitable image dataset",
                            "description": "Find and download a dataset of images for training the image recognition model. Ensure the dataset is diverse and representative of the categories you want to classify."
                        },
                        {
                            "task": "Preprocess the dataset",
                            "description": "Preprocess the dataset by resizing images, converting to the appropriate format, and splitting it into training and validation sets."
                        }   
                    ]
                }
            ]
        },
        {
            "title": "Build the image recognition model",
            "milestones": [
                {
                    "title": "Understand the TensorFlow workflow",
                    "tasks": [
                        {
                            "task": "Learn about TensorFlow basics",
                            "description": "Study the fundamental concepts of TensorFlow, such as tensors, operations, and computational graphs."
                        },
                        {
                            "task": "Understand the TensorFlow Datasets API",
                            "description": "Learn how to load and preprocess data using the TensorFlow Datasets API."
                        }
                    ]
                },
                {
                    "title": "Implement the model architecture",
                    "tasks": [
                        {
                            "task": "Choose a suitable model architecture",
                            "description": "Research and select an appropriate deep learning model architecture for image recognition, such as convolutional neural networks (CNNs)."
                        },
                        {
                            "task": "Define the model layers",
                            "description": "Define the layers of the chosen model architecture using TensorFlow's high-level APIs."
                        }
                    ]
                },
                {
                    "title": "Train the model",
                    "tasks": [
                        {
                            "task": "Set up the training pipeline",
                            "description": "Configure the training pipeline, including data augmentation, loss function, optimizer, and metrics."
                        },
                        {
                            "task": "Train the model on the dataset",
                            "description": "Train the model on the preprocessed dataset, monitoring the training progress and adjusting hyperparameters as needed."
                        }
                    ]
                },
                {
                    "title": "Evaluate the model",
                    "tasks": [
                        {
                            "task": "Evaluate the model on the validation set",
                            "description": "Evaluate the trained model's performance on the validation set and analyze the results."
                        },
                        {
                            "task": "Fine-tune the model if necessary",
                            "description": "If the model's performance is not satisfactory, fine-tune the architecture, hyperparameters, or consider additional data augmentation techniques."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Deploy the model as a web service",
            "milestones": [
                {
                    "title": "Learn Flask basics",
                    "tasks": [
                        {
                            "task": "Understand Flask fundamentals",
                            "description": "Study the basics of Flask, including routing, templates, and handling HTTP requests."
                        },
                        {
                            "task": "Learn about Flask extensions",
                            "description": "Explore Flask extensions that can simplify tasks like file uploads, form handling, and user authentication."
                        }
                    ]
                },
                {
                    "title": "Integrate the TensorFlow model with Flask",
                    "tasks": [
                        {
                            "task": "Load the trained model in Flask",
                            "description": "Load the trained TensorFlow model in the Flask application and prepare it for making predictions."
                        },
                        {
                            "task": "Implement image upload and prediction",
                            "description": "Create Flask routes and handlers for uploading images and obtaining predictions from the loaded model."
                        }
                    ]
                },
                {
                    "title": "Build the user interface",
                    "tasks": [
                        {
                            "task": "Learn HTML, CSS, and JavaScript basics",
                            "description": "Study the fundamentals of HTML, CSS, and JavaScript to create a user-friendly interface for image classification."
                        },
                        {
                            "task": "Integrate the UI with Flask",
                            "description": "Integrate the user interface with the Flask application, allowing users to upload images and view predictions."
                        }
                    ]
                },
                {
                    "title": "Deploy the web service",
                    "tasks": [
                        {
                            "task": "Choose a hosting platform",
                            "description": "Select a hosting platform for deploying the Flask web service, such as a cloud provider or a local server."
                        },
                        {
                            "task": "Deploy the Flask application",
                            "description": "Deploy the Flask application to the chosen hosting platform, ensuring it is accessible and functioning correctly."
                        }
                    ]
                }
            ]
        }
    ]



def get_roadmap(project_id, user_id):

    enroll_object = mongo_handle.is_user_enrolled(user_id, project_id)
    print(enroll_object)
    if enroll_object and enroll_object["generateRoadmap"]:
        roadmap_data = mongo_handle.get_roadmap_data(enroll_object["_id"])
        
    elif enroll_object:
        model = RoadmapClaude()
        project_object = mongo_handle.get_project_object(project_id)
        description = project_object["description"]
        skill_marks = mongo_handle.get_quiz_responses(enroll_id=enroll_object["_id"])
        
        # roadmap_data = generate_roadmap(description, skill_marks)
        try:
            print("Generating Roadmap via Claude")
            roadmap_data = model(description, skill_marks)
        except:
            print("Error generating roadmap")
            roadmap_data = None
        
        if roadmap_data:
            mongo_handle.put_roadmap_object(enroll_object["_id"], roadmap_data)
        mongo_handle.update_enroll_object(project_id, user_id)
        
    else:
        return False
    return roadmap_data