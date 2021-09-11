import sklearn.pipeline
from sklearn.model_selection import cross_validate

def cv_cps(model, X_train, y_train, features):

    """Given a model and a set of features
    print out the train and test scores from validation.

    Also, refit to entire dataset, and print out coefficients
    """

    cv_fsm = cross_validate(model, X_train[features], y_train, cv=4, return_train_score=True)
    print('Train Scores')
    print(cv_fsm['train_score'])
    print(cv_fsm['train_score'].mean())
    print(cv_fsm['train_score'].std())
    print('##########################')
    print('Test Scores')
    print(cv_fsm['test_score'])
    print(cv_fsm['test_score'].mean())
    print(cv_fsm['test_score'].std())
    print('##########################')

    if type(model) != sklearn.pipeline.Pipeline:
        model.fit(X_train[features], y_train)
        print('Coefficients from fit on full train set')
        print(model.coef_, model.intercept_)

