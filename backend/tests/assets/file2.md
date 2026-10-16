# Linear Regression

A linear regression is a linear approximation of a causal relationship between two or more variables.

Each time you create a regression, it should be meaningful.

## Process

- Get sample data
- Design a model that works for that sample
- Make predictions for the whole [[Population]]

There are:

- a [[Dependent variable]] $Y$ being predicted
- independent variables $X = \{ x_1, x_2, \ldots, x_k \}$, or predictors

$$
Y = F(x_1, x_2, \ldots, x_k)
$$

The dependent variable $Y$ is a function of the independent variables $x_1$ to $x_k$.

When using regression analysis, we want to predict the value of $Y$, provided we have the value of $X$. But to have a regression, $Y$ must depend on $X$ in some causal way. Whenever there is a change in $X$, that change must translate into a change in $Y$.

## Simple Linear Regression Model

$$
Y = \beta_0 + \beta_1 x_1 + \epsilon
$$

where $Y$ is a dependent variable and $x_1$ is an [[independent variable]].

Coefficients:

- $\beta_1$ quantifies the effect of the independent variable
- $\beta_0$ is a constant
- $\epsilon$ is the error of estimation: the difference between the observed value and the predicted value. On average, across all observations, the error is 0.

### Sample Linear Regression Equation

$$
\hat{y} = b_0 + b_1 x_1
$$

- $\hat{y}$ is an estimated / predicted value
- $b_0$ is the estimate of the regression constant $\beta_0$
- $b_1$ is the estimate of $\beta_1$. It quantifies the effect of the independent variable $x_1$ on the dependent $y$
- $x_1$ is the sample data for the independent variable

### Geometrical Representation

![[Linear Regression Model. Geometrical representation. 365 DS.png]]

## [[R Squared]]

What you will usually observe is a range of values.

In fields such as physics and chemistry, scientists are usually looking for regressions with $R^2$ between 0.7 and 0.99. In social sciences such as economics, finance, and psychology, an $R^2$ of 0.2 (20% of the variability explained by the model) can still be fantastic.

## Multiple Regression

Good models often require multiple regressions in order to address the higher complexity of problems.

### Population Model

$$
Y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_k x_k + \epsilon
$$

### Multiple Regression Equation

$$
\hat{y} = b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_k x_k
$$

## Assumptions

1. **Linearity.** Each independent variable is multiplied by a coefficient and summed up to predict the value.
2. **No endogeneity.** The covariance of the error and the $X$s is 0 for any error:

   $$
   \sigma_{X\epsilon} = 0 \quad \forall x, \epsilon
   $$

3. **Normality and homoscedasticity.** The error term is normally distributed and the [[Expected Value]] of the error is 0, as we expect to have no errors on average:

   $$
   \epsilon \sim N(0, \sigma^2)
   $$

   Homoscedasticity means constant [[Variance]].

4. **No autocorrelation.** The covariance of any two error terms is zero:

   $$
   \sigma_{\epsilon_i \epsilon_j} = 0 \quad \forall i \neq j
   $$

5. **No [[multicollinearity]].** Multicollinearity is observed when two or more variables have a high correlation with each other:

   $$
   \rho_{x_i x_j} \not\approx 1 \quad \forall i, j;\ i \neq j
   $$

### Linearity

Linear regression is the simplest non-trivial relationship.

Tip: if a scatter plot looks like it could be fitted with a curve instead of a line, linear regression is probably not an appropriate model. You could also try to transform the data.

How to fix:

1. Run a non-linear regression
2. Exponential transformation
3. Log transformation

### No Endogeneity

This refers to the prohibition of a link between the independent variables and the errors.

#### Omitted Variable Bias

Introduced to the model when you forget to include a relevant variable. As each independent variable explains $y$, they move together and are somewhat correlated. Similarly, $y$ is also explained by the omitted variable, so they are also correlated. Chances are the omitted variable is also correlated with at least one independent $x$. However, you forgot to include it as a regressor.

Everything that you don't explain with your model goes into the error. So the error becomes correlated with everything else.

How to deal with it? Answer the questions:

- Where did we draw the sample from?
- Can we get a better sample?
- Why do some strange covariations happen?

OVB:

- Always different
- Always sneaky
- Only experience and advanced knowledge can help
- Don't hesitate to ask for a hand if you can't figure it out

### Normality and Homoscedasticity

Three parts:

- **Normality:** we assume the error term is normally distributed. A normal distribution is not required for creating the regression, but for making inferences. For large samples the [[Central Limit Theorem]] applies to the error terms too.
- **Zero mean:** if the mean is not expected to be zero, then the model is not the best-fitting one. Having an intercept solves that problem.
- **Homoscedasticity** means equal variance: $\sigma_{\epsilon_1}^2 = \sigma_{\epsilon_2}^2 = \ldots = \sigma_{\epsilon_k}^2 = \sigma^2$
  - What if there was a pattern in the variance?

A way to circumvent heteroscedasticity:

- Check for OVB
- Look for [[outliers]] (and try to remove them)
- Transform (see [[Semi-log Model]] and [[Log-log Model]])

### No Autocorrelation

(No serial correlation)

$$
\sigma_{\epsilon_i \epsilon_j} = 0 \quad \forall i \neq j
$$

How does one detect autocorrelation?

- A common way is to plot all the residuals on a graph and look for patterns. If you can't find any, you're safe.
- Durbin–Watson test. Generally, its value falls between 0 and 4:
  - 2 indicates no autocorrelation
  - Values below 1 and above 3 are a cause for alarm

There is no remedy. When autocorrelation is present, avoid the linear regression model.

Other types of regressions that deal with time series data:

- Autoregressive model
- Moving average model
- Autoregressive moving average model
- Autoregressive integrated moving average model

### No [[Multicollinearity]]

$$
\rho_{x_i x_j} \approx 1 \quad \forall i, j;\ i \neq j
$$

We observe [[multicollinearity]] when two or more variables have a high correlation.

Rationale:

- if $A$ can be represented using $B$, there's no point in using both
- if $C$ can be *almost* ($\rho_{CD} \approx 0.9$) represented using $D$, there's no point in using both

How to fix:

- Drop one of the two variables
- Transform them into one variable (e.g. average price)
- Keep them both, but treat them with extreme caution

Prevention: find the correlation between each pair of independent variables.

## Rules

Usually, simplicity is better rewarded than higher explanatory power.
