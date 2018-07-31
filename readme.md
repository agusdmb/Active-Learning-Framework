Design and architecture
=======================

In this document I describe the architecture of the framework.
First I raise the decisions regarding the specificity or generality of
the software. Then I will describe the flow of the framework and its
hotspots. Finally, I give the detail of the different components.

Finding the midpoint of specificity and generality
--------------------------------------------------

### Too specific problem

A too specific Framework has the advantage of leaving less
implementation work to the programmer user. In this way, with little
effort you can be applying *Active Learning* on your data. But this gain
in effort is a consequence of decisions already made when implementing
the Framework. These decisions limit the possibilities of the user
programmer to adapt the Framework to his particular case. For this
reason a Framework of these characteristics will only be useful and
convenient to use in specific projects where the decisions taken at the
time of design and implementation coincide with the needs of the
particular project of the programmer user.

### Problem of too generic

An overly generic Framework will have the advantage of adapting to more
use cases. Making it more attractive to learn and use because it is more
versatile. But this generalization is accompanied by many design and
implementation decisions left in the hands of the user programmer. For
this reason, you must first make these decisions before you can create
an instance of the Framework. If these design and / or implementation
decisions require a lot of effort, they will discourage the programmer
user from using the framework in the first instance. Since an Ad-hoc
solution probably entails a similar effort but works better.

### Proposal

My proposal is to develop a framework that allows the programmer user to
implement instances of annotation projects based on *Automatic Learning*
with the minimum programming without losing generality. That is, achieve
a framework which can be instantiated with a minimum of effort but also
facilitating the possibility for the user programmer to adapt the same
to their particular project. For this, the framework will provide an
already established workflow and pre-programmed modules that allow
choosing different methods for its hotspots. At the same time,
interfaces will be provided so that the user can create their own
instances of the hotspots to adjust the framework even more to their
particular project.

Design of the proposed framework
--------------------------------

It is a framework architecture, with frozen spots and hotspots. The
hotspots indicate the parametrizable points of the framework, where the
user programmer will provide the required functionalities: Oracle,
Selector, Model and Dataset.

The **interfaces** are abstract classes with unimplemented methods and /
or attributes, therefore they require that a class be implemented that
implements the methods required by the interface.

![alt text][class diagram]

### Framework Flow

For the architecture of the Framework, the architecture developed by for
its case study was taken as a basis. From its architecture a similar one
was thought that admits modifications to be able to adapt it to other
projects.

In the flow diagram we can distinguish between *blue* and *red* *figures*
being these the *frozen spots* and *hotspots* respectively. The workflow
determined by the Framework can be observed as the loop formed by the frozen
spots (blue figures) in said figure. It begins by training a *model* from an
*algorithm* and *tagged data* . This model, once trained, will be evaluated
with a part of the tagged data that will be separated for this purpose, making
them not participate in the training of the model. Then we proceed to *predict*
about *untagged data*its possible labels. They will be sent to the *selector*
which will select a certain number of instances to be sent to the *oracle* .
Then this will ask the labeling user to enter the labels of each of these
instances. Once the tags have been obtained, the main loop will be started
again, this time using the original tagged data and the manually tagged data to
train the model.

![alt_text][architecture]

As we can see in Figure \[fig: flow\_diagram\] the main loop is already
determined by the framework. But it is the user programmer who decides
how these components behave in the loop. It must always provide tagged
and untagged data, but you can also adjust this loop to your needs. For
example, the user programmer can choose which *algorithm* the *model
will* be trained on , or which *selection method it will* use over the
automatically labeled instances. For this, you can use the instances
already implemented in the framework, or implement their own version of
them. So you can also do it with the *oracle* , thus personalizing the
user experience tagger.

### System Components

#### Oracle

This class is in charge of showing the oracle (labeling person) the
instances that the selector selects to label, obtain the label and
return it to the *ActiveLearner* to save the new instances labeled.

It is an abstract class, so the user must implement a class that meets
this interface and instantiate it. This new class should at least define
an attribute `target_names`. The same will be explained below together
with the rest of the methods of this class:

-   `target_names`Attribute that will contain a list with the name of
    each target class. It must correspond in order with the values ​​of
    `y`the *Dataset* attribute .

-   `ask(readable_X, recoms)`Method which will be called by the
    *ActiveLearner* in each iteration of the main loop to obtain new
    labels. It receives the following parameters:

    1.  `readable_X`It is a list that contains, for each element that
        you want to label, the output of `get_unlabeled_readable()` the
        *Dataset* method .

    2.  `recoms` It is a list with the labels predicted by the model to
        use as a label recommendation to the oracle.

    This method will call for each element that is passed to the other
    methods of this class to process the elements to be displayed and
    validate the labels.

-   `ask_for_element(x, recom)`This method is called internally by each
    element that is passed to the `ask()`previously described method to
    process each element individually. Its parameters are:

    1.  `x`Element information obtained by the method
        `get_unlabeled_readable()`of *Dataset* .

    2.  `recom` The label predicted by the model to use as a
        recommendation for oracle.

-   `show_options()` Print the possible labels, with their names and
    numbers that represent them for each one.

-   `show_element(x, recom)`This method shows the data with a simple
    screen printing and its predicted label. It is recommended to
    reimplement this method to customize the oracle's user experience.

    1.  `x`Element information obtained by the method
        `get_unlabeled_readable()`of *Dataset* .

    2.  `recom` The label predicted by the model to use as a
        recommendation for oracle.

-   `validate_answer(answer)` This method controls that the oracle has
    entered a valid label.

The programmer user is encouraged to reimplement methods
`show_element()`and `show_options()`in conjunction with the method
`get_unlabeled_readable()`of *Dataset* to adapt the display of labels
and instances the context of particular labeling of each project.

put the gui, triangulation, and I do not know more, I'll go scoring here
...

#### Selector

Although it is a simple module, it is the heart of *Active Learning* .
It is an interface that specifies the requirements for the functionality
that selects the instances that are going to be sent to the *Oracle* for
labeling, based on the information provided by the model on a dataset.
This interface requires only the following method:

-   `select(model, data, n)`This method receives the trained model, the
    data on which to select and the amount of data to be selected.
    Returns a list with the indexes of the selected elements.

    1.  `model`It is an instance that satisfies the interest of Model,
        which has already been trained (the method has already been
        called `fit()`).

    2.  `data`Are the data returned by the method `get_unlabeled()` of
        *Dataset* .

    3.  `n` It is an integer number specifying the amount of data to be
        selected.

The user programmer can instantiate selectors whenever he implements
this interface. However, the framework provides selectors already
implemented, ready to be instantiated in this hotspot, they are
described below:

*UncertaintySelector:* Selects the instances over which the model has
less security. That is, for which the highest probability log is low. It
serves for when the nuclei are already well defined, to deillimitate the
edges.

*CertaintySelector:* Selects the instances on which the model has
greater security. That is, those with the high probability log is
higher. It is very useful for the first iterations since, as he explains
PAPER OF WHO HE EXPLAINS, he better characterizes the nuclei of the
classes.

*MinDiffSelector:* select the ones with the *smallest* difference
between the class with the highest probability and the second class with
the highest probability

*EntropySelector:* based on theory of Shanon information. select the
instances with the most entropy. the formula: - Sum (ci \* log (ci))
becomes 0 for labeled classes and becomes larger the more similar the
probabilities of each class are.

*CommitteeSelector:* It is used in conjunction with the CommitteeModel
which contains a list of models, for average operations the average of
the labels is calculated, and for the selector in question the data of
each of the models is passed.

*ClusteringSelector:* Implement

*RandomSelector:* Select instances randomly, this is to compare the
effectiveness of Active Learning using different selectors, against this
method that would be not to do Active Learning, since when choosing
randomly the instances to label it is as if we were simply labeling
instances to improve the learning the model.

, section 4.2 summarizes Settles ... how to explain this here?

this paper tmb is good <https://arxiv.org/pdf/1702.08540.pdf>

#### Model

This module is an interface that specifies the requirements for the
machine learning algorithm that will be used to train a prediction model
from the training dataset. It will run at the beginning of each loop of
the main loop to train a new model. And then it will be called again to
predict the labels on the untrained data. This module has been designed
in such a way that an already trained instance of it can be passed as an
argument to ActiveLearner. In this way we can train on a server where
the time of use has a high cost, and can be labeled locally to avoid
using it. This also allows us to use pre-trained instances which are
increasingly common.

To instantiate an object of this class it is necessary that the
programming user implements the methods described in the interface. They
are:

-   `fit(X, y)` Adjust the model to the training data.

    1.  `X`It is the training data, which is returned by the
        `get_X()`Dataset method .

    2.  `y`The objectives of the training data, which it returns
        `get_y()`from the Dataset.

    This method returns nothing.

-   `predict(X)`It predicts the kinds of data it receives as input.
    Returns a list with the predicted class for each element.

-   `predict_proba(X)`Predicts the probabilities of each class of the
    data it receives. Returns for each element in X a list of n-uplas
    where n is the number of target classes in the project and where
    each value n is the probability that the element is of that class.

-   `score(X, y)`Returns the average precision on the data `X`with the
    objectives `y`. `X`and `y`must have the same type that `X`and
    `y`training.

These methods are equivalent to those used by the scikit-learn library,
mostly classifiers. For this reason, in this hotspot these methods can
be used by directly invoking them with those provided by the
scikit-learn classifiers or by implementing their own following the
interface described above.

Training is always done in batch, not incremental, because there are
very few algorithms that have their incremental training version and
also because in this way we allow the portion of the corpus that is used
for evaluation to be changed.

#### Dataset

This module will contain the data labeled to train, and the non-tagged
data on which to apply active learning.

It is the only class that needs at least that the user programmer
initialize, passing as parameters the tagged and untagged data. In turn,
the user programmer can inherit from this class to reimplement some of
the same methods.

To improve the efficiency of this class, it was decided to internally
store the variables `X`and `X_unlabeled`in the same variable, called
`X`. Since these must be of the same type, and contain information of
the same type as well (the characteristics of each instance) this is not
a problem, and in turn makes us gain a lot of time, since otherwise,
every time an instance is tagged (or a selection of instances) they must
be removed from `X_unlabeled`and added to `X.`But this generates a large
overhead, since these data are immutable so you have to create new
instances each time. With this implementation we solve this problem by
keeping the data in the same variable, and accessing them using masks,
one to access the `X` original and another to access the`X_unlabeled` we
managed to label a new instance as easy as changing the masks.

In the same way, the `y`one stored in this class not only contains the
labels of the tagged data, but also functions as a mask. In it a value
is stored for each element in `X,` this value can be the label of that
data (to be a value between 0 and n-1 with n the number of classes) or
it can be -1 indicating that the label is not contained of that data, or
-2 indicating that this data has already been shown to label but the
oracle has not been able to determine exactly the label of the same,
ignoring it.

Therefore the correct form of accder to `X`(tagged data used to train)
already `X_unlabeled`(data on which to select) is through the methods
`get_X()`and `get_unlabeled()`. In this way, the data is saved
internally outside this module.

-   `__init__(X, y, X_unlabeled)`this function is executed when a new
    instance of the class is created. It requires 4 mandatory parameters
    and two optional ones. They are described below:

    1.  `X`It contains the data on which the label is held. It must be a
        ndarray instance of the numpy or csr\_matrix library of the
        scipy library.

    2.  `y`It contains, in the same order as `X,`the labels of said
        data. It must be a ndarray instance of the numpy library.

    3.  `X_unlabeled`It contains the data of which the label is not
        possessed and on which it is desired to select to label. It must
        be an instance of the same type as `X`.

    4.  `test_size`Optional parameter. Determines the percentage of
        training data that will be separated to be used as model
        evaluation. They will be snapped when the class is intact and
        will not be used for training at any time.

    5.  `random_state`Optional parameter. It is the seed that is used to
        divide the training data leaving a percentage of them to
        evaluate.

-   `_split_X(X, y, test_size, random_state)`This method must be called
    only internally and in the initialization of the class. It is the
    one that performs the separation of the data of training in two, to
    train and to evaluate. The same to do it uses the
    `train_test_split()`sklearn function .

-   `get_X()` Method to access the training data from outside, using the
    mask described in the introduction of this module.

-   `get_y()`Method to obtain the values ​​of the training data labels.
    Use the mask described in the description of this module internally.

-   `get_unlabeled()`Method to obtain the untagged data, and also have
    not been ignored to tag before. Use inside the mask described in the
    introduction of this module for this purpose.

-   `tag_elements(indices, tags)`Method to add new tags to the data they
    were in `X_unlabeled.`. The parameters of this function are
    described below:

    1.  `indices`It has the indices that they give with the tagged data
        filtered by the mask. This is to overshadow the inner workings
        of this class.

    2.  `tags`List with the values ​​of the labels of the data whose
        indexes were passed. They must have the same order.

-   `get_unlabeled_readable(i)`This method will be called when
    requesting the labels of some element to the oracle. It receives the
    parameter i which is the index of the element to be presented in the
    *Oracle* . It must return what is necessary to be able to show the
    object to the user, for example, if it is images, this method could
    return the location of said image so that the *Oracle can* then
    display it.

-   `_get_train_indices()`Method to be used only within the class. It
    returns a list with the indexes of the elements in variable X that
    are data labeled for training. It is used for the mask.

-   `_get_unlabeled_indices()`Method to be used only within the class.
    It returns a list with the indexes of the elements in variable X
    that are untagged data. It is used for the mask.

#### Active Learner

This is the module that connects all the previous ones. To create an
instance, you must first create an instance of each of the previous
modules to pass them as a parameter. This class is fully implemented,
and has the following methods:

-   `fit()`This method calls the method `fit()`of the model that was
    passed to it as a parameter at the time of initialization of the
    instance or by which it was changed with the method
    `change_selector()`. To the same happens as parameters `X`e `y`to
    train, obtained from the method `get_X()`and `get_y()`the `dataset`.

-   `select(n)`This method is to select the non-annotated data that will
    go to the oracle for its annotation. It receives an n as an input
    parameter that specifies the number of instances that the selector
    has to return. The method calls the method `select()`from
    `Selector`which it also passes the trained model and the untagged
    data (obtained through the interface `get_unlabeled()`and returns
    the output thereof).

-   `ask(indices)`This method searches for the requested non-annotated
    instances (indices) `Dataset`through its method
    `get_unlabeled_readable()`. Then calculate the label predicted by
    him `Model`and these two parameters are passed `Oracle`through the
    method `ask()`.

-   `tag_elements(indices, y)`This method receives the indexes of the
    elements that the method `get_unlabeled()`of the `Dataset`
    `(indices)`and the corresponding label returns to each one of these
    instances `(y)`. What makes the method is called the method
    `tag_elements()`of `Dataset`.

-   `get_scores()`Method that returns a list with the values ​​of the
    score of each one `fit()`made.

-   `change_selector()`This method receives a new instance of the
    `Selector`parameter and changes it `ActiveLearner`to the current one
    for future selections.

Evaluation
----------

When you create an instance of `Dataset`the training dataset, it is
divided into two. From these parts one will be used to train the model
and another to evaluate the accuracy of the model. With the part that is
left to evaluate at no time will the model be trained. This part will
serve so that at the end of each iteration of the main loop the labels
are predicted on them, then they are compared with the original labels
and the percentage of success of the model is calculated. These values
​​are stored in a list, to then graph and analyze the performance
throughout the iterations.

The percentage of data left for tests is defined by initializing the
instance of `Dataset`passing it as a parameter in `test_size`a value
between 0 and 1 indicating the percentage that is left for test. By
default, this value is 0.2, which translates to 20% of the data being
left for testing.

Future work could be cross validation? (or not, xq if you start with few
data then the ones labeled using the selector of greater certainty makes
a very high validation obtained when you are constantly adding new data
about which the model predicts with much security)

Input format
------------

Since generality is sought, the framework will not provide features
extraction features, but it is expected that users provide the
vectorized dataset, ie a list of instances where each in turn is a list
containing the values ​​of the features.

[architecture]: https://writelatex.s3.amazonaws.com/nfzhskrjkrsm/uploads/533/24106368/1.jpg?X-Amz-Expires=14400&X-Amz-Date=20180727T152342Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJF667VKUK4OW3LCA/20180727/us-east-1/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=e448e7c2a5b65c1abe6dd2d5eda085c67315ed0c06fd2d3b0ebf2763d30a8b38 "Architecture"
[class diagram]: https://writelatex.s3.amazonaws.com/nfzhskrjkrsm/uploads/1287/24531380/1.jpg?X-Amz-Expires=14400&X-Amz-Date=20180727T152348Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJF667VKUK4OW3LCA/20180727/us-east-1/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=6c160b86cf07916319b4a75da39542551c6538559bc26d5eaabeab68ebefb22a "Class Diagram"
