# Sophie's Value Chain WebApp Project Development Repo

* **Developer**: [Sophie Du](https://github.com/chuandu2)
* **QA**: [Kejin Qian](https://github.com/kejin-qian)
----------------------------------------------------------------

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)

<!-- tocstop -->

## Project Charter 

### **Vision**:

To predict used car values for sellers and buyers.

### **Mission**:

Enable users to input features of the used cars they are interested in (car age, vehicle type, gear box, etc.) and generate the predicted value based on their entries.

### **Success criteria**:

Users can clearly understand the meanings of the features that need inputs, and successfully get predicted used car values within 10 seconds each time based on their entries. Optimize the predictive model for predicting the used car prices to achieve reasonably high cross-validation accuracy above 80% of price predictions and low Mean Square Error (MSE).

## Project Backlog

### **Theme 1**
The 1st theme of this project is to explore the historical data of used cars including the features that determine the values of the cars, and construct predictive models for predicting used car prices based on user inputs by trying diverse models (linear model, regularized regression models, tree models) and selecting the final model with best performance for later use in the WebApp.

### **Epics**

**Epic 1: Exploratory Data Analysis** *(planned for next 2 weeks)*

In this section, data manipulations will be performed to explore the relationships among variables and determine the subset of variables to be included in the predictive models.

<*Stories*>

*  *Data Overview:* drop useless columns, check descriptive statistics of variables, do visualizations to see distributions of variables and detect outliers and skewness. (1 point)
* *Data Cleansing:* remove unwanted observations (duplicated and irrelevant), fix structural errors (typos or inconsistent capitalization), filter outliers, and impute or remove missing values (numeric and categorical). (2 points)

**Epic 2: Feature Engineering** *(planned for next 2 weeks)*

In this section, new features will be created based on interactions and correlations among existed variables.

<*Stories*>

* *Variable Relationships:* check correlations among variables and detect multicollinearity. (1 point)
*  *Feature Creation:* create interaction features (products, sums, differences, etc.), combine sparse classes for categorical variables by grouping similar classes, add dummy variables based on necessity, and remove unused features. (2 points)

**Epic 3: Model Construction**

In this section, different models will be built based on the cleaned data for predicting used car prices, and important features for predicting prices will be determined, which will be used as user inputs for the user engagement on the WebApp.

<*Stories*>

(Data Preparation and Initial Model Selection are planned for next 2 weeks)

* *Data Preparation:* split the data into training data and testing data. (0 point) 
* *Initial Model Selection:*  besides the most basic linear regression model, several effective machine learning algorithms for regression tasks will be trained on the training data, including regularized regression models (Lasso, Ridge, Elastic-Net) and tree models (Decision Tree, Random Forests, Boosted Trees). (1 points)
* *Fit & Tune Models:* for each model, for each set of selected parameters, perform 10-fold cross-validation using the training set and calculate the cross-validation error. (4 points)
* *Find Model Representatives:* for each model, check the set of parameter values which yields the lowest cross-validation errors, so that the representatives for each type of the potential models with their corresponding best parameters have been selected. (1 point)

**Epic 4: Model Performances & Evaluations**

In this section, the best model among all models for predicting used car prices will be selected through performance evaluations and comparisons.

<*Stories*>

* *Performance Metrics:* for each representative model, predict on the testing set. Calculate performance metrics (MSE: Mean Squared Error will be used, the lower the better) for the predictions, and choose the best model. (2-4 points)
* *Final Model Selection:* 10 replicates of 10-fold cross validation will be performed on the representative models so that the predictive power of each model can be assessed using the same partition of cross-validation, and the final best model with lowest cross-validation error will be selected for predicting used car values in the WebApp. (2 points)

### **Theme 2**
The 2nd theme of this project is to build a WebApp which enables users to predict used car prices based on their inputs for related features. The detailed steps will be updated when we get to learn more on this.

**WebApp Building**

In this section, the WebApp for predicting used car values based on user inputs will be developed step by step, from the start of product planning to the end of testing and experiments.

<*Stories*> (Stories below are from the 'intro-to-avc' lecture slide)

* Product Planning
* Write Code → **Development Cycle & QA**
	* Branches & pull requests
	* **Logging**  
	* Write **unit tests** and **model reproducibility tests**  
	* **Version control**: code, configurations, and data input (shared repo!)  
	* Schedule jobs → **Scheduling**  
	* **Documentation**
* Tests pass locally
* `requirements.txt`  →  **Dependency / environment management**  
*   Put code in a test environment →  **Integration testing**
*   Run the tests
*   Put code in a scalable production environment →  **Deployment, scalability**
*   Run code… →  **Execution**
*   Monitor application and retrain model when necessary →  **Ops and monitoring**
*   Automate all the things →  **Automation**
*   A/B test →  **A/B testing and Design of Experiments**
*   Sprint review and retrospective (at the end of sprints) →  **Agile**
*   Profit !!!
