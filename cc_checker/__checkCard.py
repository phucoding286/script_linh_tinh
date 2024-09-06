from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier



class CardPredict:
    def __init__(self, path_train="train.txt"):
        self.path_train = path_train

    
    def read_train(self):
        X_train, y_train = [], []
        with open(self.path_train, "r", encoding="utf-8") as file:
            data = file.read().splitlines()
            for info in data:
                X_train.append(info.split(" </split> ")[0])
                y_train.append(info.split(" </split> ")[1])
        return [X_train], y_train
    
    
    def predict(self, card_info):
        X_train, y_train = self.read_train()
        bow_transformer = CountVectorizer(analyzer="char")
        X_train = bow_transformer.fit_transform(X_train[0]).toarray()
        desicion_tree = DecisionTreeClassifier()
        random_forest = RandomForestClassifier()
        bayes_model = GaussianNB()
        svm_model = SVC(probability=True)
        knn_model = KNeighborsClassifier(n_neighbors=3)
        voting_model = VotingClassifier(estimators=[("desicion tree", desicion_tree),
                                                    ("random forest", random_forest),
                                                    ("svm", svm_model),
                                                    ("knn", knn_model),
                                                    ("bayes", bayes_model)], voting="soft")
        voting_model.fit(X_train, y_train)
        X_test = bow_transformer.transform([card_info]).toarray()
        predict = voting_model.predict(X_test)
        return predict[0]