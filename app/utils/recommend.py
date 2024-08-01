from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.mongo import MongoHandle
import os


class SkillMatcher:
    def __init__(self, projects):
        self.projects = projects
        self.skills = self.__load_skill_mappings()
        self.mlb = MultiLabelBinarizer(classes=self.skills)
        self.projects_skills = [{project['projectId']: project['skills']} for project in projects]
        self.projects_skills_encoded = self.__encode_project_skills()

    def __load_skill_mappings(self):
        """
        Load skills from a txt file and create mapping to one hot
        """
        with open(os.path.join('data','skills.txt'), 'r') as file:
            skills = file.read().splitlines()
        return skills

    def __encode_project_skills(self):
        all_project_skills = [list(project.values())[0] for project in self.projects_skills]
        encoded_skills = self.mlb.fit_transform(all_project_skills)
        return encoded_skills

    def match_skills(self, user_skills, n):
        """
        Match user skills with project skills and sort them by cosine similarity and return top n
        """
        user_skills_encoded = self.mlb.transform([user_skills])[0]
        similarities = cosine_similarity([user_skills_encoded], self.projects_skills_encoded)[0]
        
        # Get top n matches
        top_n_indices = similarities.argsort()[-n:][::-1]
        top_n_projects = [self.projects[i] for i in top_n_indices]
        
        return top_n_projects


class Recommender():
    def __init__(self) -> None:
        self.mongo = MongoHandle()
        self.projects = self.mongo.get_all_projects()
        self.users = None
        self.enrollment = None
        self.ratings = None
        self.skill_matcher = SkillMatcher(self.pro)
    
    def __getEnrolledProjects(self, user):
        """
        Get enrolled projects for a given user.
        """
        enrollments = self.mongo.get_user_enrollments(user)
        projects = []
        for enroll in enrollments:
            projects.append(self.mongo.get_project_object(enroll))
        
        return projects

    def __applyscheme(self, user, schemes):
        """
        Apply the recommendation scheme to the data.
        """
        recommended_projects = self.projects.copy()

        for scheme in schemes:
            if scheme == 'role':
                recommended_projects = self.__applyRuleRoleFilter(user, recommended_projects)
            elif scheme == 'difficulty':
                recommended_projects = self.__applyRuleDifficultyFilter(user, recommended_projects)
            else:
                raise ValueError(f"Invalid recommendation scheme: {scheme}")
    
    def __applyRuleRoleFilter(self, user, projects):
        """
        Apply role-based filtering to the projects.
        """
        return [project for project in projects if user['role'] in project['roles']]
    
    def __applyRuleDifficultyFilter(self, user, projects):
        """
        Apply difficulty-based filtering to the projects.
        """
        vals = {"easy": 0, "intermediate": 1, "difficult": 2}
        enrolled_difficulties = [vals[i["difficulty"]] for i in self.__getEnrolledProjects(user)]
        avg_difficulty = sum(enrolled_difficulties) // len(avg_difficulty)
        return [project for project in projects if vals[project['difficulty']] >= avg_difficulty]
    
    def __applyRuleSkillMatchFilter(self, user, projects):
        """
        Apply skill-based filtering to the projects.
        """
        user_skills = user['skills']
        return [project for project in projects if all(skill in user_skills for skill in project['skills'])]

    def getRecommendations(self, user: dict, recommendationSchemes: list[int]) -> list[int]:
        """
        Get a list of recommended projects for a given user.

        Parameters:
        user (int): The unique identifier of the user for whom recommendations are needed.
        recommendationScheme (list[int]) : A sequence of recommendation schemes to apply

        Returns:
        list[int]: A list of project IDs recommended for the given user.
        """
        # Implement recommendation logic here
        # This method should return a list of recommended projects for the given user
        pass

