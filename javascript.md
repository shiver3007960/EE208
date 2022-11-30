# Javascript #
[](#)
对象[‘属性名’]

删除对象的属性可以使用delete关键字，格式如下：delete 对象.属性名

for (var 变量 in 对象) {
 
}

JavaScript中一共有5种基本数据类型：String、Number、 Boolean、Undefined、Null。

function 函数名([形参1,形参2,...,形参N]) {
    语句...
}

使用 函数表达式 来创建一个函数（比较常用）

var 函数名  = function([形参1,形参2,...,形参N]) {
    语句....
}
示例代码：

var fun  = function() {
    console.log("这是我的第三个函数");
}
在函数中return后的语句都不会执行，如果return语句后不跟任何值就相当于返回一个undefined，如果函数中不写return，则也会返回undefined，return后可以跟任意类型的值

立即执行函数：函数定义完，立即被调用，这种函数叫做立即执行函数，立即执行函数往往只会执行一次。

(function () {
    alert("我是一个匿名函数");
})();

解析器在调用函数每次都会向函数内部传递进一个隐含的参数，这个隐含的参数就是this，this指向的是一个对象，这个对象我们称为函数执行的上下文对象，根据函数的调用方式的不同，this会指向不同的对象
```
// 使用工厂模式创建对象
function createPerson(name, age) {
    // 创建新的对象
    var obj = new Object();
    // 设置对象属性
    obj.name = name;
    obj.age = age;
    // 设置对象方法
    obj.sayName = function () {
        console.log(this.name);
    };
    //返回新的对象
```
 >当以函数的形式调用时，this是window.当以方法的形式调用时，谁调用方法this就是谁.当以构造函数的形式调用时，this就是新创建的那个对象.我们可以使用 instanceof 运算符检查一个对象是否是一个类的实例，它返回true或false

语法格式：

对象 instanceof 构造函数

原型:
```
// 使用构造函数来创建对象
function Person(name, age) {
    // 设置对象的属性
    this.name = name;
    this.age = age;
}

// 在Person类的原型对象中添加方法
Person.prototype.sayName = function() {
    console.log(this.name);
};
```

 那原型（prototype）到底是什么呢？

我们所创建的每一个函数，解析器都会向函数中添加一个属性prototype，这个属性对应着一个对象，这个对象就是我们所谓的原型对象，即显式原型，原型对象就相当于一个公共的区域，所有同一个类的实例都可以访问到这个原型对象，我们可以将对象中共有的内容，统一设置到原型对象中。

如果函数作为普通函数调用prototype没有任何作用，当函数以构造函数的形式调用时，它所创建的对象中都会有一个隐含的属性，指向该构造函数的原型对象，我们可以通过__proto__（隐式原型）来访问该属性。当我们访问对象的一个属性或方法时，它会先在对象自身中寻找，如果有则直接使用，如果没有则会去原型对象中寻找，如果找到则直接使用。

以后我们创建构造函数时，可以将这些对象共有的属性和方法，统一添加到构造函数的原型对象中，这样不用分别为每一个对象添加，也不会影响到全局作用域，就可以使每个对象都具有这些属性和方法了。

访问一个对象的属性时，先在自身属性中查找，找到返回， 如果没有，再沿着__proto__这条链向上查找，找到返回，如果最终没找到，返回undefined，这就是原型链，又称隐式原型链，它的作用就是查找对象的属性(方法)。

我们使用一张图来梳理一下上一节原型案例的代码：

注意：Object对象是所有对象的祖宗，Object的原型对象指向为null，也就是没有原型对象

###### toString() ######
toString()函数用于将当前对象以字符串的形式返回。该方法属于Object对象，由于所有的对象都"继承"了Object的对象实例，因此几乎所有的实例对象都可以使用该方法，所有主流浏览器均支持该函数。

// 使用构造函数来创建对象
function Person(name, age) {
    // 设置对象的属性
    this.name = name;
    this.age = age;
}


###### hasOwnProperty方法 ######

前边章节我们学过，如何遍历一个对象所有的属性和值，那我们要是判断当前对象是否包含指定的属性或方法可以使用 in 运算符来检查，如下代码演示：


 如果我只想要检查自身对象是否含有某个方法或属性，我们可以使用Object的hasOwnProperty()方法，它返回一个布尔值，判断对象是否包含特定的自身（非继承）属性。如下代码演示：

// 创造一个构造函数
function MyClass() {
}
 
// 向MyClass的原型中添加一个name属性
MyClass.prototype.name = "我是原型中的名字";
 
// 可以使用对象的hasOwnProperty()来检查对象自身中是否含有该属性，使用该方法只有当对象自身中含有属性时，才会返回true


###### 对象继承 ######

* 借用构造函数继承:使用.call()和.apply()将父类构造函数引入子类函数，使用父类的构造函数来增强子类实例，等同于复制父类的实例给子类

1. 定义父类型构造函数
2. 定义子类型的构造函数
3. 给子类型的原型添加方法
4. 创建子类型的对象然后调用

借用构造函数继承的重点就在于SuperType**.call(this, name)**，调用了SuperType构造函数，这样，SubType的每个实例都会将SuperType中的属性复制一份。
```
// 定义父类型构造函数
function SuperType(name) {
    this.name = name;
    this.showSupperName = function () {
        console.log(this.name);
    };
}

// 定义子类型的构造函数
function SubType(name, age) {
    // 在子类型中调用call方法继承自SuperType
    SuperType.call(this, name);
    this.age = age;
}
 
// 给子类型的原型添加方法
SubType.prototype.showSubName = function () {
    console.log(this.name);
};
 
// 创建子类型的对象然后调用
var subType = new SubType("孙悟空", 20);
subType.showSupperName();
subType.showSubName();
console.log(subType.name);
console.log(subType.age);
```
> 缺点描述：1、只能继承父类的实例属性和方法，不能继承原型属性和方法 2、无法实现构造函数的复用，每个子类都有父类实例函数的副本，影响性能，代码会臃肿
2.12.7.3、组合继承
核心思想： 原型链+借用构造函数的组合继承

1. 利用原型链实现对父类型对象的方法继承
2. 利用super()借用父类型构建函数初始化相同属性

```
function Person(name, age) {
    this.name = name;
    this.age = age;
}
 
Person.prototype.setName = function (name) {
    this.name = name;
};
 
function Student(name, age, price) {
    Person.call(this, name, age); // 为了得到父类型的实例属性和方法
    this.price = price; // 添加子类型私有的属性
}
 
Student.prototype = new Person(); // 为了得到父类型的原型属性和方法
Student.prototype.constructor = Student; // 修正constructor属性指向
Student.prototype.setPrice = function (price) { // 添加子类型私有的方法 
    this.price = price;
};
 
```

###### 垃圾回收 ######

在JS中拥有自动的垃圾回收机制，会自动将这些垃圾对象从内存中销毁，我们不需要也不能进行垃圾回收的操作，我们需要做的只是要将不再使用的对象设置null即可。

###### 创建数组 ######

* var arr = new Array();
* var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]; &nbsp;可以不同类型
###### 数组方法 ######

* push()方法：可以向数组的末尾添加一个或多个元素，并返回数组的新的长度
```var result = arr.push("唐僧", "蜘蛛精", "白骨精", "玉兔精");```

* pop()方法：该方法可以删除数组的最后一个元素，并将被删除的元素作为返回值返回

* unshift()方法：该方法向数组开头添加一个或多个元素，并返回新的数组长度

```var result = arr.unshift("牛魔王", "二郎神");```

* shift()方法：该方法可以删除数组的第一个元素，并将被删除的元素作为返回值返回

* forEach()方法需要一个函数作为参数，像这种函数，由我们创建但是不由我们调用的，我们称为回调函数。数组中有几个元素函数就会执行几次，每次执行时，浏览器会将遍历到的元素，以实参的形式传递进来，我们可以来定义形参，来读取这些内容，浏览器会在回调函数中传递三个参数:当前正在遍历的元素,当前正在遍历的元素的索引,正在遍历的数组
```
var arr = ["孙悟空", "猪八戒", "沙和尚"];
arr.forEach(function (value, index, obj) {
    console.log(value + " #### " + index + " #### " + obj);
});
```
* slice()方法：该方法可以用来从数组提取指定元素，该方法不会改变元素数组，而是将截取到的元素封装到一个新数组中返回

* splice()方法：该方法可以用于删除数组中的指定元素，该方法会影响到原数组，会将指定元素从原数组中删除，并将被删除的元素作为返回值返回.第一个参数：表示开始位置的索引 第二个参数：表示要删除的元素数量 第三个参数及以后参数：可以传递一些新的元素，这些元素将会自动插入到开始位置索引前边

* concat()方法演示：该方法可以连接两个或多个数组，并将新的数组返回，该方法不会对原数组产生影响

* join()方法演示：该方法可以将数组转换为一个字符串，该方法不会对原数组产生影响，而是将转换后的字符串作为结果返回，在join()中可以指定一个字符串作为参数，这个字符串将会成为数组中元素的连接符，如果不指定连接符，则默认使用，作为连接符
```
var arr = ["孙悟空", "猪八戒", "沙和尚"];
var result = arr.join("@-@");
```
* reverse()方法：该方法用来反转数组（前边的去后边，后边的去前边），该方法会直接修改原数组

* sort()方法演示：该方法可以用来对数组中的元素进行排序，也会影响原数组，默认会按照Unicode编码进行排序.注意：即使对于纯数字的数组，使用sort()排序时，也会按照Unicode编码来排序，所以对数字进排序时，可能会得到错误的结果。

>我们可以自己来指定排序的规则，我们可以在sort()添加一个回调函数，来指定排序规则，回调函数中需要定义两个形参，浏览器将会分别使用数组中的元素作为实参去调用回调函数，使用哪个元素调用不确定，但是肯定的是在数组中a一定在b前边，浏览器会根据回调函数的返回值来决定元素的顺序，如下：

        如果返回一个大于0的值，则元素会交换位置
        如果返回一个小于0的值，则元素位置不变
        如果返回一个等于0的值，则认为两个元素相等，也不交换位置
>经过上边的规则，我们可以总结下：

        如果需要升序排列，则返回 a-b
        如果需要降序排列，则返回 b-a

###### 函数对象 ######

call()和apply()这两个方法都是函数对象的方法，需要通过函数对象来调用，当对函数调用call()和apply()都会调用函数执行，在调用call()和apply()可以将一个对象指定为第一个参数，此时这个对象将会成为函数执行时的this，call()方法可以将实参在对象之后依次传递，apply()方法需要将实参封装到一个数组中统一传递，如下演示：
```
var obj = {
    name: "obj",
    sayName: function () {
        console.log(this.name);
    }
};

fun(2, 3);
fun.call(obj, 2, 3);
```

> 注意：默认fun()函数调用，this指向的是window对象，你可以使用call()调用函数，在调用的时候传入一个对象，这个对象就是this所指向的对象，也就是说，可以自己指定this的指向，然后从第二个参数开始，实参将会依次传递


###### arguments参数 ######
在调用函数时，浏览器每次都会传递进两个隐含的参数：函数的上下文对象： this, 封装实参的对象： arguments.arguments是一个类数组对象，它也可以通过索引来操作数据，也可以获取长度，在调用函数时，我们所传递的实参都会在arguments中保存，比如：arguments.length 可以用来获取实参的长度，我们即使不定义形参，也可以通过arguments来使用实参，只不过比较麻烦，例如：arguments[0]：表示第一个实参.arguments[1]：表示第二个实参.
它里边有一个属性叫做callee，这个属性对应一个函数对象，就是当前正在指向的函数的对象。

```
function fun(a, b) {
    console.log(arguments.callee);
    console.log(arguments.callee == fun);
}
```

###### Date对象 ######
在JavaScript中使用Date对象来表示一个时间，如果直接使用构造函数创建一个Date对象，则会封装为当前代码执行的时间。

```
var date = new Date();
console.log(date);
 
date.getFullYear();//获取当前日期对象的年份(四位数字年份)
date.getMonth();//获取当前日期对象的月份(0 ~ 11)
date.getDate();//获取当前日期对象的日数(1 ~ 31)
date.getHours();//获取当前日期对象的小时(0 ~ 23)
date.getMinutes();//获取当前日期对象的分钟(0 ~ 59)
date.getSeconds();//获取当前日期对象的秒钟(0 ~ 59)
date.getMilliseconds();//获取当前日期对象的毫秒(0 ~ 999)
```


###### Math对象 ######

* Math.PI
* Math.E
* Math.abs(1))       //可以用来计算一个数的绝对值
* Math.ceil(1.1))    //可以对一个数进行向上取整，小数位只有有值就自动进1
* Math.floor(1.99))   //可以对一个数进行向下取整，小数部分会被舍掉
* Math.round(1.4))    //可以对一个数进行四舍五入取整
* Math.abs(-1))       //可以用来计算一个数的绝对值
* Math.ceil(-1.1))    //可以对一个数进行向上取整，小数部分会被舍掉
* Math.floor(-1.99))  //可以对一个数进行向下取整，小数位只有有值就自动进1
* Math.round(-1.4))   //可以对一个数进行四舍五入取整
* Math.random()：可以用来生成一个0-1之间的随机数
* 生成一个0-x之间的随机数：Math.round(Math.random()*x)
* 生成一个x-y之间的随机数：Math.round(Math.random()*(y-x)+x)
* Math.round(Math.random() * 10));            //生成一个0-10之间的随机数
* Math.round(Math.random() * (10 - 1) + 1));  //生成一个1-10之间的随机数
* Math.pow(12, 3));   //Math.pow(x,y)：返回x的y次幂
* Math.sqrt(4));      //Math.sqrt(x) ：返回x的平方根


###### String对象 ######

* charAt()方法：该方法可以根据索引获取指定位置的字符
* charCodeAt()方法：该方法获取指定位置字符的字符编码（Unicode编码）
* concat()方法：该方法可以用来连接两个或多个字符串
* indexof()方法演示：该方法可以检索一个字符串中是否含有指定内容，如果字符串中含有该内容，则会返回其第一次出现的索引，如果没有找到指定的内容，则返回-1，可以指定一个第二个参数，指定开始查找的位置
* lastIndexOf()方法演示：该方法的用法和indexOf()一样，不同的是indexOf是从前往后找，而lastIndexOf是从后往前找，也可以指定开始查找的位置
* slice()方法：可以从字符串中截取指定的内容，不会影响原字符串，而是将截取到内容返回
* substring()方法：可以用来截取一个字符串，它和slice()类似
* substr()方法演示：该方法用来截取字符串.第一个参数：截取开始位置的索引.第二个参数：截取的长度
* split()方法演示：该方法可以将一个字符串拆分为一个数组，需要一个字符串作为参数，将会根据该字符串去拆分数组
* toUpperCase()方法演示：将一个字符串转换为大写并返回
* toLowerCase()方法演示：将一个字符串转换为小写并返回

###### RegExp对象 ######

`var 变量名 = new RegExp("正则表达式","匹配模式");`

匹配模式：

* i：忽略大小写
* g：全局匹配模式
* ig：忽略大小写且全局匹配模式

`var 变量名 = /正则表达式/匹配模式`
匹配模式：

* i：忽略大小写
* g：全局匹配模式
* m：执行多行匹配

* split()方法演示：该方法可以将一个字符串拆分为一个数组，方法中可以传递一个正则表达式作为参数，这样方法将会根据正则表达式去拆分字符串，这个方法即使不指定全局匹配，也会全都插分

* search()方法演示：该方法可以搜索字符串中是否含有指定内容，如果搜索到指定内容，则会返回第一次出现的索引，如果没有搜索到返回-1，它可以接受一个正则表达式作为参数，然后会根据正则表达式去检索字符串，serach()只会查找第一个，即使设置全局匹配也没用

* match()方法演示：该方法可以根据正则表达式，从一个字符串中将符合条件的内容提取出来，默认情况下我们的match()只会找到第一个符合要求的内容，找到以后就停止检索，我们可以设置正则表达式为全局匹配模式，这样就会匹配到所有的内容，可以为一个正则表达式设置多个匹配模式，且顺序无所谓，match()会将匹配到的内容封装到一个数组中返回，即使只查询到一个结果
 
* replace()方法演示：该方法可以将字符串中指定内容替换为新的内容，默认只会替换第一个，但是可以设置全局匹配替换全部.第一个参数：被替换的内容，可以接受一个正则表达式作为参数,第二个参数：新的内容


##### DOM #####

* document.getElementById(id) 	通过元素 id 来查找元素。
* document.getElementsByTagName(name) 	通过标签名来查找元素,返回数组。
* document.getElementsByClassName(name) 	通过类名来查找元素，返回数组。
* document.querySelector(CSS选择器)	通过CSS选择器选择一个元素。
* document.querySelectorAll(CSS选择器) 	通过CSS选择器选择多个元素，返回数组。
###### 获取 HTML 的值 ######

* 元素节点.innerText	获取 HTML 元素的 inner Text。
* 元素节点.innerHTML 	获取 HTML 元素的 inner HTML。
* 元素节点.属性	获取 HTML 元素的属性值。
* 元素节点.getAttribute(attribute)	获取 HTML 元素的属性值。
* 元素节点.style.样式	获取 HTML 元素的行内样式值。


> 注意：如果CSS的样式名中含有-，这种名称在JS中是不合法的比如background-color，需要将这种样式名修改为驼峰命名法，去掉-，然后将-后的字母大写，我们通过style属性设置的样式都是行内样式，同样的获取也是行内样式，而行内样式有较高的优先级，所以通过JS修改的样式往往会立即显示，但是如果在样式中写了!important，则此时样式会有最高的优先级，即使通过JS也不能覆盖该样式，此时将会导致JS修改样式失效，所以尽量不要为样式添加!important

> 通过style属性设置和读取的都是内联样式，无法读取样式表中的样式或者说正在应用的样式，如果想要读取当前正在应用的样式属性我们可以使用元素.currentStyle.样式名来获取元素的当前显示的样式，它可以用来读取当前元素正在显示的样式，如果当前元素没有设置该样式，则获取它的默认值，但是currentStyle只有IE浏览器支持，其它的浏览器都不支持，在其它浏览器中可以使用getComputedStyle()这个方法来获取元素当前的样式，这个方法是window的方法，可以直接使用，但是需要两个参数：第一个参数：要获取样式的元素 第二个参数：可以传递一个伪元素，一般都传null.该方法会返回一个对象，对象中封装了当前元素对应的样式，可以通过 对象.样式名 来读取样式，如果获取的样式没有设置，则会获取到真实的值，而不是默认值，比如：没有设置width，它不会获取到auto，而是一个长度，但是该方法不支持IE8及以下的浏览器。通过currentStyle和getComputedStyle()读取到的样式都是只读的，不能修改，如果要修改必须通过style属性，因此，我们可以写一个适配各个浏览器的读取元素样式的方法。

###### 改变 HTML 的值 ######

* 元素节点.innerText = new text content	改变元素的 inner Text。
* 元素节点.innerHTML = new html content	改变元素的 inner HTML。
* 元素节点.属性 = new value	改变 HTML 元素的属性值。
* 元素节点.setAttribute(attribute, value)	改变 HTML 元素的属性值。
* 元素节点.style.样式 = new style	改变 HTML 元素的行内样式值。

修改节点的内容除了常用的innerHTML和innerText之外，还有insertAdjacentHTML和insertAdjacentText方法，可以在指定的地方插入内容。insertAdjacentText方法与insertAdjacentHTML方法类似，只不过是插入纯文本，参数相同。
```
object.insertAdjacentHTML(where,html);
object.insertAdjacentText(where,text);
```
```
where：
beforeBegin：插入到开始标签的前面
beforeEnd：插入到结束标签的前面
afterBegin：插入到开始标签的后面
afterEnd：插入到结束标签的后面
```

> 这两个方法必须等文档加载好后才能执行，否则会出错.insertAdjacentText只能插入普通文本，insertAdjacentHTML插入html代码。使用insertAdjacentHTML方法插入script脚本文件时，必须在script元素上定义defer属性。使用insertAdjacentHTML方法插入html代码后，页面上的元素集合将发生变化.insertAdjacentHTML方法不适用于单个的空的元素标签(如img，input等)

    /*获取任意标签的内容*/
    function getInnerText(element) {
        // 判断浏览器是否支持textContent,如果支持，则使用textContent获取内容，否则使用innerText获取内容。
        if (typeof element.textContent == "undefined") {
            return element.innerText;
        } else {
            return element.textContent;
        }
    }

    /*设置任意标签的内容*/
    function setInnerText(element, text) {
        // 判断浏览器是否支持textContent,如果支持，则使用textContent设置内容，否则使用innerText设置内容。
        if (typeof element.textContent == "undefined") {
            return element.innerText = text;
        } else {
            return element.textContent = text;
        }
    }


###### 修改 HTML 元素 ######
	
* document.createElement(element)	创建 HTML 元素节点。	
* document.createAttribute(attribute)	创建 HTML 属性节点。	
* document.createTextNode(text)	创建 HTML 文本节点。	
* 元素节点.removeChild(element)	删除 HTML 元素。	
* 元素节点.appendChild(element)	添加 HTML 元素。	
* 元素节点.replaceChild(element)	替换 HTML 元素。	
* 元素节点.insertBefore(element)	在指定的子节点前面插入新的子节点。	

###### 动态判断、添加、删除、切换样式 ######

 
    btn0.onclick = function () {
        alert(hasClass(box, "b2"));
    };
 
    btn1.onclick = function () {
        addClass(box, "b2");
    };
 
    btn2.onclick = function () {
        removeClass(box, "b2");
    };
 
    btn3.onclick = function () {
        toggleClass(box, "b2");
    };
 
    /*
     * 判断一个元素中是否含有指定的class属性值
     * 如果有该class，则返回true，没有则返回false
     */
    function hasClass(obj, cn) {
        var reg = new RegExp("\\b" + cn + "\\b");
        return reg.test(obj.className);
    }
 
    /*
     * 向一个元素中添加指定的class属性值
     * 参数:
     * 	obj 要添加class属性的元素
     *  cn 要添加的class值
     */
    function addClass(obj, cn) {
        // 检查obj中是否含有cn
        if (!hasClass(obj, cn)) {
            obj.className += " " + cn;
        }
    }
 
    /*
     * 删除一个元素中的指定的class属性
     */
    function removeClass(obj, cn) {
        var reg = new RegExp("\\b" + cn + "\\b");
        obj.className = obj.className.replace(reg, "");
    }
 
    /*
     * toggleClass可以用来切换一个类
     * 	如果元素中具有该类，则删除
     * 	如果元素中没有该类，则添加
     */
    function toggleClass(obj, cn) {
        // 判断obj中是否含有cn
        if (hasClass(obj, cn)) {
            // 存在，则删除
            removeClass(obj, cn);
        } else {
            // 没有，则添加
            addClass(obj, cn);
        }
    }

###### 查找 HTML 父子 #####

* 元素节点.parentNode	返回元素的父节点。
* 元素节点.parentElement	返回元素的父元素。
* 元素节点.childNodes	返回元素的一个子节点的数组（包含空白文本Text节点）。
* 元素节点.children	返回元素的一个子元素的集合（不包含空白文本Text节点）。
* 元素节点.firstChild	返回元素的第一个子节点（包含空白文本Text节点）。
* 元素节点.firstElementChild	返回元素的第一个子元素（不包含空白文本Text节点）。
* 元素节点.lastChild	返回元素的最后一个子节点（包含空白文本Text节点）。
* 元素节点.lastElementChild	返回元素的最后一个子元素（不包含空白文本Text节点）。
* 元素节点.previousSibling	返回某个元素紧接之前节点（包含空白文本Text节点）。
* 元素节点.previousElementSibling	返回指定元素的前一个兄弟元素（相同节点树层中的前一个元素节点）。
* 元素节点.nextSibling	返回某个元素紧接之后节点（包含空白文本Text节点）。
* 元素节点.nextElementSibling	返回指定元素的后一个兄弟元素（相同节点树层中的下一个元素节点）。

 兼容性方法：

    /*获取任意一个父级元素的第一个子元素*/
    function getfirstElementChild(element) {
        if(element.firstElementChild) {
            return element.firstElementChild;
        } else {
            var node = element.firstChild;
            while(node && node.nodeType != 1) {
                node = node.nextSibling;
            }
            return node;
        }
    }
    
    /*获取任意一个父级元素的最后一个子元素*/
    function getLastElementChild(element) {
        if(element.lastElementChild) {
            return element.lastElementChild;
        } else {
            var node = element.lastChild;
            while(node && node.nodeType != 1) {
                node = node.previousSibling;
            }
            return node;
        }
    }
 
    /*获取任意一个子元素的前一个兄弟元素*/
    function getPreviousElementSibling(element) {
        if(element.previousElementSibling) {
            return element.previousElementSibling;
        } else {
            var node = element.previousSibling;
            while(node && node.nodeType != 1) {
                node = node.previousSibling;
            }
            return node;
        }
    }
    
    /*获取任意一个子元素的后一个兄弟元素*/
    function getNextElementSibling(element) {
        if(element.nextElementSibling) {
            return element.nextElementSibling;
        } else {
            var node = element.nextSibling;
            while(node && node.nodeType != 1) {
                node = node.nextSibling;
            }
            return node;
        }
    }

##### DOM文档事件 #####

###### 窗口事件 由窗口触发该事件 (同样适用于 <body> 标签)：######

* onblur	当窗口失去焦点时运行脚本。
* onfocus	当窗口获得焦点时运行脚本。
* onload	当文档加载之后运行脚本。
* onresize	当调整窗口大小时运行脚本。
* onstorage	当 Web Storage 区域更新时（存储空间中的数据发生变化时）运行脚本。

###### 表单事件 ######

* onblur	当元素失去焦点时运行脚本。
* onfocus	当元素获得焦点时运行脚本。
* onchange	当元素改变时运行脚本。
* oninput	当元素获得用户输入时运行脚本。
* oninvalid	当元素无效时运行脚本。
* onselect	当选取元素时运行脚本。
* onsubmit	当提交表单时运行脚本。
```  
onblur = function () {
        this.style.background = "green";
        }
```
##### 键盘事件 #####

* onkeydown	当按下按键时运行脚本。
* onkeyup	当松开按键时运行脚本。
* onkeypress	当按下并松开按键时运行脚本。
案例演示1：当键盘按下判断当前的按键是不是 a ，如果是就输出true，否则输出false

    <script>
        /* 当键盘按下判断当前的按键是不是 a ，如果是就输出true，否则输出false */
        window.onkeydown = function (event) {
            /* 解决兼容性问题 */
            event = event || window.event;
    
            if (event.keyCode == 65) {
                console.log("true");
            } else {
                console.log("false");
            }
        };
    </script>

> 当事件的响应函数被触发时，浏览器每次都会将一个事件对象作为实参传递进响应函数。Event 对象代表事件的状态，比如事件在其中发生的元素、键盘按键的状态、鼠标的位置、鼠标的状态。解决事件对象的兼容性问题：event = event || window.event;

键鼠属性：

* ctrlKey	返回当事件被触发时，“CTRL” 键是否被按下。
* altKey	返回当事件被触发时，“ALT” 是否被按下。
* shiftKey	返回当事件被触发时，“SHIFT” 键是否被按下。
* clientX	返回当事件被触发时，鼠标指针的水平坐标。
* clientY	返回当事件被触发时，鼠标指针的垂直坐标。
* screenX	返回当某个事件被触发时，鼠标指针的水平坐标。
* screenY	返回当某个事件被触发时，鼠标指针的垂直坐标。
###### 鼠标事件 #####

* onclick	当单击鼠标时运行脚本。
* ondblclick	当双击鼠标时运行脚本。
* onmousedown	当按下鼠标按钮时运行脚本。
* onmouseup	当松开鼠标按钮时运行脚本。
* onmousemove	当鼠标指针移动时运行脚本。
* onmouseover	当鼠标指针移至元素之上时运行脚本，不可以阻止冒泡。
* onmouseout	当鼠标指针移出元素时运行脚本，不可以阻止冒泡。
* onmouseenter	当鼠标指针移至元素之上时运行脚本，可以阻止冒泡。
* onmouseleave	当鼠标指针移出元素时运行脚本，可以阻止冒泡。
* onmousewheel	当转动鼠标滚轮时运行脚本。
* onscroll	当滚动元素的滚动条时运行脚本。
案例演示1：创建一个正方形div，默认颜色为黑色，当鼠标移入div，背景颜色变为红色，当鼠标移出div，背景颜色变为绿色

    /* 当鼠标移出div，背景颜色变为绿色 */
    box.onmouseleave = function () {
        this.style.background = "green";
    };
</script>
</body>
</html>
通用的拖拽元素函数，创建两个div，进行拖拽演示.

    <script>

        /*
        * 提取一个专门用来设置拖拽的函数
        * 参数：开启拖拽的元素
        */
        function drag(obj) {
            //当鼠标在被拖拽元素上按下时，开始拖拽
            obj.onmousedown = function (event) {
                // 解决事件的兼容性问题
                event = event || window.event;
    
                // 设置obj捕获所有鼠标按下的事件
                /**
                 * setCapture()：
                 * 只有IE支持，但是在火狐中调用时不会报错，
                 * 而如果使用chrome调用，它也会报错
                 */
                obj.setCapture && obj.setCapture();
    
                // obj的偏移量 鼠标.clentX - 元素.offsetLeft
                // obj的偏移量 鼠标.clentY - 元素.offsetTop
                var ol = event.clientX - obj.offsetLeft;
                var ot = event.clientY - obj.offsetTop;
    
                // 为document绑定一个鼠标移动事件
                document.onmousemove = function (event) {
                    // 解决事件的兼容性问题
                    event = event || window.event;
                    // 当鼠标移动时被拖拽元素跟随鼠标移动
                    // 获取鼠标的坐标
                    var left = event.clientX - ol;
                    var top = event.clientY - ot;
                    // 修改obj的位置
                    obj.style.left = left + "px";
                    obj.style.top = top + "px";
                };
    
                // 为document绑定一个鼠标松开事件
                document.onmouseup = function () {
                    // 取消document的onmousemove事件
                    document.onmousemove = null;
                    // 取消document的onmouseup事件
                    document.onmouseup = null;
                    // 当鼠标松开时，取消对事件的捕获
                    obj.releaseCapture && obj.releaseCapture();
                };
    
                /*
                * 当我们拖拽一个网页中的内容时，浏览器会默认去搜索引擎中搜索内容，
                * 此时会导致拖拽功能的异常，这个是浏览器提供的默认行为，
                * 如果不希望发生这个行为，则可以通过return false来取消默认行为，
                * 但是这招对IE8不起作用
                */
                return false;
            };
        }
    </script>
    </body>
    </html>


###### 媒体事件 ######
通过视频（videos），图像（images）或音频（audio） 触发该事件。

* onabort	当发生中止事件时运行脚本。
* oncanplay	当媒介能够开始播放但可能因缓冲而需要停止时运行脚本。
* oncanplaythrough	当媒介能够无需因缓冲而停止即可播放至结尾时运行脚本。
* ondurationchange	当媒介长度改变时运行脚本。
* onemptied	当媒介资源元素突然为空时（网络错误、加载错误等）运行脚本。
* onended	当媒介已抵达结尾时运行脚本。
* onerror	当在元素加载期间发生错误时运行脚本。
* onloadeddata	当加载媒介数据时运行脚本。
* onloadedmetadata	当媒介元素的持续时间以及其它媒介数据已加载时运行脚本。
* onloadstart	当浏览器开始加载媒介数据时运行脚本。
* onpause	当媒介数据暂停时运行脚本。
* onplay	当媒介数据将要开始播放时运行脚本。
* onplaying	当媒介数据已开始播放时运行脚本。
* onprogress	当浏览器正在取媒介数据时运行脚本。
* onratechange	当媒介数据的播放速率改变时运行脚本。
* onreadystatechange	当就绪状态（ready-state）改变时运行脚本。
* onseeked	当媒介元素的定位属性不再为真且定位已结束时运行脚本。
* onseeking	当媒介元素的定位属性为真且定位已开始时运行脚本。
* onstalled	当取回媒介数据过程中（延迟）存在错误时运行脚本。
* onsuspend	当浏览器已在取媒介数据但在取回整个媒介文件之前停止时运行脚本。
* ontimeupdate	当媒介改变其播放位置时运行脚本。
* onvolumechange	当媒介改变音量亦或当音量被设置为静音时运行脚本。
* onwaiting	当媒介已停止播放但打算继续播放时运行脚本。
###### 其它事件 ######

* onshow	当 <menu> 元素在上下文显示时触发。
* ontoggle	当用户打开或关闭 <details> 元素时触发。
###### 事件冒泡 ######

事件的冒泡（Bubble）：所谓的冒泡指的就是事件的向上传导，当后代元素上的事件被触发时，其祖先元素的相同事件也会被触发，在开发中大部分情况冒泡都是有用的，如果不希望发生事件冒泡可以通过事件对象来取消冒泡。

1. 创建两个div，叠放在一起，分别绑定单击事件，点击最里边的div，不会触发两个div的单击事件，只会触发自己的单击事件，这时候我们可以取消事件冒泡

    <script>
        var div1 = document.getElementById("div1");
        var div2 = document.getElementById("div2");
    
        // 为div1绑定单击事件
        div1.onclick = function () {
            console.log("div1 的单击事件触发了！");
            stopBubble();
        };
    
        // 为div2绑定单击事件
        div2.onclick = function () {
            console.log("div2 的单击事件触发了！");
            stopBubble();
        };
    
        // 取消事件冒泡
        function stopBubble(event) {
            // 如果提供了事件对象，则这是一个非IE浏览器
            if (event && event.stopPropagation) {
                // 因此它支持W3C的stopPropagation()方法
                event.stopPropagation();
            } else {
                // 否则，我们需要使用IE的方式来取消事件冒泡
                window.event.cancelBubble = true;
            }
        }
    </script>

2. 当点击a标签的时候，阻止a标签的默认跳转事件，采用事件阻止

<!-- 在这里写JavaScript代码，因为JavaScript是由上到下执行的 -->
<script>
    var a = document.getElementById("a");
 
    // 为a绑定单击事件
    a.onclick = function () {
        stopDefault();
    };
 
    // 阻止浏览器的默认行为
    function stopDefault(event) {
        if (event && event.preventDefault) {
            // 阻止默认浏览器动作(W3C)
            event.preventDefault();
        } else {
            // IE中阻止函数器默认动作的方式
            window.event.returnValue = false;
        }
        return false;
    }
</script>
</body>
</html>

###### 事件委派 ######
我们希望只绑定一次事件，即可应用到多个的元素上，即使元素是后添加的，我们可以尝试将其绑定给元素的共同的祖先元素，也就是事件的委派。事件的委派，是指将事件统一绑定给元素的共同的祖先元素，这样当后代元素上的事件触发时，会一直冒泡到祖先元素，从而通过祖先元素的响应函数来处理事件。事件委派是利用了事件冒泡，通过委派可以减少事件绑定的次数，提高程序的性能。

1. 为ul列表中的所有a标签都绑定单击事件
<!-- 在这里写JavaScript代码，因为JavaScript是由上到下执行的 -->
<script>
    var u1 = document.getElementById("u1");
 
    // 为ul绑定一个单击响应函数
    u1.onclick = function (event) {
        event = event || window.event;
        // 如果触发事件的对象是我们期望的元素，则执行，否则不执行
        if (event.target.className == "link") {
            console.log("我是ul的单击响应函数");
        }
    };
</script>
</body>
</html>

image-20201021134924509

###### 事件绑定 ######
我们以前绑定事件代码只能一个事件绑定一个函数，那我们要是想一个事件对应多个函数，并且不存在兼容性的问题该如何解决呢？

接下来，我会直接提供两个已经编写好的事件绑定和事件解绑的兼容性代码，如下：

    /*为元素绑定事件兼容性代码*/
    function addEventListener(element, type, fn) {
        if(element.addEventListener) {
            element.addEventListener(type, fn, false);
        } else if(element.attachEvent) {
            element.attachEvent("on" + type, fn);
        } else {
            element["on" + type] = fn;
        }
    }
    
    /*为元素解绑事件兼容性代码*/
    function removeEventListener(element, type, fnName) {
        if(element.removeEventListener) {
            element.removeEventListener(type, fnName, false);
        } else if(element.detachEvent) {
            element.detachEvent("on" + type, fnName);
        } else {
            element["on" + type] = null;
        }
    }

案例演示：为按钮1的单击事件绑定两个函数，然后点击按钮2取消按钮1的单机事件绑定函数f1


##### BOM概述 #####

* Window：代表的是整个浏览器的窗口，同时window也是网页中的全局对象
* Navigator：代表的当前浏览器的信息，通过该对象可以来识别不同的浏览器
* Location：代表当前浏览器的地址栏信息，通过Location可以获取地址栏信息，或者操作浏览器跳转页面
* History：代表浏览器的历史记录，可以通过该对象来操作浏览器的历史记录，由于隐私原因，该对象不能获取到具体的历史记录，只能操作浏览器向前或向后翻页，而且该操作只在当次访问时有效
* Screen：代表用户的屏幕的信息，通过该对象可以获取到用户的显示器的相关的信息
* 这些BOM对象在浏览器中都是作为window对象的属性保存的，可以通过window对象来使用，也可以直接使用。

###### Window对象 ######
5.2.1、弹出框
JavaScript 有三种类型的弹出框：警告框、确认框和提示框。

###### 警告框 ######
如果要确保信息传递给用户，通常会使用警告框。当警告框弹出时，用户将需要单击“确定”来继续。
语法

`window.alert("sometext");`

###### 确认框 ######

如果您希望用户验证或接受某个东西，则通常使用“确认”框。
当确认框弹出时，用户将不得不单击“确定”或“取消”来继续进行。
如果用户单击“确定”，该框返回 true。如果用户单击“取消”，该框返回 false。

`window.confirm("sometext")`
注意：window.confirm() 方法可以不带 window 前缀来编写。
###### 提示框 ######

如果您希望用户在进入页面前输入值，通常会使用提示框。
当提示框弹出时，用户将不得不输入值后单击“确定”或点击“取消”来继续进行。
如果用户单击“确定”，该框返回输入值。如果用户单击“取消”，该框返回 NULL。

`window.prompt("sometext","defaultText");`
window.prompt() 方法可以不带 window 前缀来编写。

###### 定时事件 ######


`setTimeout(function, milliseconds)`在等待指定的毫秒数后执行函数。

`setInterval(function, milliseconds)`等同于 setTimeout()，但持续重复执行该函数。

setTimeout() 方法：延时器
`window.setTimeout(function, milliseconds);`
注意：window.setTimeout() 方法可以不带 window 前缀来编写。

setInterval() 方法在每个给定的时间间隔重复给定的函数。

`window.setInterval(function, milliseconds);`
注意：window.setInterval() 方法可以不带 window 前缀来写。

###### 常用窗口属性 ######

这两个属性都以像素返回尺寸：

* window.innerHeight - 浏览器窗口的内高度（以像素计）
* window.innerWidth - 浏览器窗口的内宽度（以像素计）
浏览器窗口（浏览器视口）不包括工具栏和滚动条。

###### 其它窗口方法 ######
window.open() ：打开新的窗口

`window.open(URL,name,specs,replace);`

    <script>
        function openWin() {
            myWindow = window.open('', '', 'width=200,height=100');
            myWindow.document.write("<p>这是新建窗口</p>");
        }
    </script>

`window.close() ：关闭当前窗口`

`window.moveTo() ：移动当前窗口`

`window.resizeTo() ：调整当前窗口`
l>


###### Location对象 ######
Location对象中封装了浏览器的地址栏的信息，如果直接打印location，则可以获取到地址栏的信息（当前页面的完整路径）


* location         //输出location对象
* location.href)    //输出当前地址的全路径地址
* location.origin)  //输出当前地址的来源
* location.protocol) //输出当前地址的协议
* location.hostname) //输出当前地址的主机名
* location.host)   //输出当前地址的主机
* location.port)    //输出当前地址的端口号
* location.pathname) //输出当前地址的路径部分
* location.search)  //输出当前地址的?后边的参数部分

###### 常用方法 ######
* assign()：用来跳转到其它的页面，作用和直接修改location一样

`location.assign("https://www.baidu.com");`
* reload()：用于重新加载当前页面，作用和刷新按钮一样，如果在方法中传递一个true，作为参数，则会强制清空缓存刷新页面
`location.reload(true);`
* replace()：可以使用一个新的页面替换当前页面，调用完毕也会跳转页面，它不会生成历史记录，不能使用回退按钮回退
`location.replace("https://www.baidu.com");`

##### Exception #####


* name	设置或返回错误名
* message	设置或返回错误消息（一条字符串）

|错误名|描述|
|:-:|:-:|
|EvalError|已在 eval() 函数中发生的错误|
|RangeError|已发生超出数字范围的错误|
|ReferenceError|已发生非法引用|
|SyntaxError|已发生语法错误|
|TypeError|已发生类型错误|
|URIError|在 encodeURI() 中已发生的错误|
```
try {
    // 可能发生异常的代码
} catch (error) {
    // 发生错误执行的代码
} finally {
    // 无论是否出错都会执行的代码
```

然而有时候我们在检测到一些不合理的情况发生的时候也可以主动抛出错误，请使用 throw 关键字抛出来主动抛出异常。

thow后面就是我们要抛出的异常对象，在以前的时候都是出现错误的时候浏览器抛出异常对象，只是现在是我们自己主动抛出的异常对象。

> 主动抛出内置异常
    /*该函数接收一个数字，返回它的平方。*/
    function foo(num) {
        if (typeof num == "number") {
            return num * num;
        } else {
            throw new TypeError("您输入的是一个非法数字！")
        }
    }

console.log(foo(4));


6.1.4.2、主动抛出自定义异常

如果要自定义错误类型，只需要继承任何一个自定义错误类型都可以，一般直接继承Error即可。

    /*自定义错误*/
    function MyError(message) {
        this.message = "注意：这是自定义的错误"
        this.name = "自定义错误";
    }
    MyError.prototype = new Error();

    try {
        throw new MyError("注意：这是自定义错误类型")
    } catch (error) {
        console.log(error.message)
    }


#### JSON ####
##### 概述 #####
JSON：JavaScript Object Notation（JavaScript 对象标记法），它是一种存储和交换数据的语法。

当数据在浏览器与服务器之间进行交换时，这些数据只能是文本，JSON 属于文本并且我们能够把任何 JavaScript 对象转换为 JSON，然后将 JSON 发送到服务器。我们也能把从服务器接收到的任何 JSON 转换为 JavaScript 对象。以这样的方式，我们能够把数据作为 JavaScript 对象来处理，无需复杂的解析和转译。

##### JSON语法 #####
在json中，每一个数据项，都是由一个键值对（或者说是名值对）组成的，但是键必须是字符串，且由双引号包围，而值必须是以下数据类型之一：

* 字符串（在 JSON 中，字符串值必须由双引号编写）
* 数字
* 对象（JSON 对象）
* 数组
* 布尔
* null
JSON 的值不可以是以下数据类型之一：
* 函数
* 日期
* undefined
因为 JSON 语法由 JavaScript 对象标记法衍生而来，所以很少需要其它额外的软件来处理 JavaScript 中的 JSON。

##### JSON 对象 #####
JSON 中的值可以是对象，JSON 中作为值的对象必须遵守与 JSON 对象相同的规则。

{
    "employee": {"name": "Bill Gates", "age": 62, "city": "Seattle"}
}

##### JSON 数组 #####
JSON 中的值可以是数组。

{
    "employees": ["Bill", "Steve", "David"]
}

##### JSON字符串转JS对象 #####
JSON.parse()：可以将以JSON字符串转换为JS对象，它需要一个JSON字符串作为参数，会将该字符串转换为JS对象并返回
##### JS对象转JSON字符串 #####
JSON.stringify()：可以将一个JS对象转换为JSON字符串，需要一个js对象作为参数，会返回一个JSON字符串
```
var obj = {name: "猪八戒", age: 28, gender: "男"};
var jsonStr = JSON.stringify(obj);
```

#### AJAX ####
##### AJAX概述 #####
传统的web交互是用户触发一个http请求服务器，然后服务器收到之后，在做出响应到用户，并且返回一个新的页面，每当服务器处理客户端提交的请求时，客户都只能空闲等待，并且哪怕只是一次很小的交互、只需从服务器端得到很简单的一个数据，都要返回一个完整的HTML页，而用户每次都要浪费时间和带宽去重新读取整个页面。这个做法浪费了许多带宽，由于每次应用的交互都需要向服务器发送请求，应用的响应时间就依赖于服务器的响应时间，这导致了用户界面的响应比本地应用慢得多。

AJAX 的出现,刚好解决了传统方法的缺陷，AJAX 是一种用于创建快速动态网页的技术，通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新，这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

##### AJAX的XMLHttpRequest对象 #####
AJAX 的核心是 XMLHttpRequest 对象。 所有现代浏览器都支持 XMLHttpRequest 对象。

XMLHttpRequest 对象用于幕后同服务器交换数据，这意味着可以更新网页的部分，而不需要重新加载整个页面。

创建 XMLHttpRequest 的语法是：

variable = new XMLHttpRequest();

> 但是需要注意的是，出于安全原因，现代浏览器不允许跨域访问，这意味着尝试加载的网页和 XML 文件都必须位于相同服务器上。

##### AJAX的XMLHttpRequest对象方法 ####

* new XMLHttpRequest()	创建新的 XMLHttpRequest 对象
* abort()	取消当前请求
* getAllResponseHeaders()	返回头部信息
* getResponseHeader()	返回特定的头部信息
* open(method, url, async, user, psw)	规定请求method：请求类型 GET 或 POST
* url：文件位置
* async：true（异步）或 false（同步）
* user：可选的用户名
* psw：可选的密码
* send()	将请求发送到服务器，用于 GET 请求
* send(string)	将请求发送到服务器，用于 POST 请求
* setRequestHeader()	向要发送的报头添加标签/值对
* 
##### AJAX的XMLHttpRequest对象属性 #####

1. onreadystatechange	定义当 readyState 属性发生变化时被调用的函数
  
2. readyState	保存 XMLHttpRequest 的状态。
* 0：请求未初始化
* 1：服务器连接已建立
* 2：请求已收到
* 3：正在处理请求
* 4：请求已完成且响应已就绪
  
3. responseText	以字符串返回响应数据
4. responseXML	以 XML 数据返回响应数据
  
5. status	返回请求的状态号
* 200: "OK"
* 403: "Forbidden"
* 404: "Not Found"
  
6. statusText	返回状态文本（比如 “OK” 或 “Not Found”）
##### AJAX的GET请求 #####


    //步骤一：创建异步对象
    var ajax = new XMLHttpRequest();
    //步骤二：设置请求的url参数，参数一是请求的类型，参数二是请求的url
    ajax.open("get", "users.json");
    //步骤三：发送请求
    ajax.send();
    //步骤四：注册事件 onreadystatechange 状态改变就会调用
    ajax.onreadystatechange = function () {
        if (ajax.readyState == 4 && ajax.status == 200) {
            //步骤五：如果能够进到这个判断，说明数据完美的回来了，并且请求的页面是存在的
            console.log(ajax.responseText);//输入响应的内容
        }
    };


##### AJAX的POST请求 #####
工程结构：

    users.json

    [
    {"name":"孙悟空","age":18,"gender":"男"},
    {"name":"猪八戒","age":19,"gender":"男"},
    {"name":"唐僧","age":20,"gender":"男"},
    {"name":"沙和尚","age":21,"gender":"男"}
    ]

    index.html

    //步骤一：创建异步对象
    var ajax = new XMLHttpRequest();
    //步骤二：设置请求的类型及url，注意：post请求一定要添加请求头才行不然会报错
    ajax.open("post", "users.json");
    ajax.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //步骤三：发送请求
    ajax.send();
    //步骤四：注册事件 onreadystatechange 状态改变就会调用
    ajax.onreadystatechange = function () {
        //步骤五：如果能够进到这个判断，说明数据完美的回来了，并且请求的页面是存在的
        if (ajax.readyState == 4 && ajax.status == 200) {
            console.log(ajax.responseText);//输入响应的内容
        }
    };
##### AJAX的请求整合 #####

    users.json

    [
    {"name":"孙悟空","age":18,"gender":"男"},
    {"name":"猪八戒","age":19,"gender":"男"},
    {"name":"唐僧","age":20,"gender":"男"},
    {"name":"沙和尚","age":21,"gender":"男"}
    ]

    index.html

    var Ajax = {
        get: function (url, fn) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200 || xhr.status == 304) {
                    fn.call(this, xhr.responseText);
                }
            };
            xhr.send();
        },
        post: function (url, data, fn) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
                    fn.call(this, xhr.responseText);
                }
            };
            xhr.send(data);
        }
    };

    // 演示GET请求
    Ajax.get("users.json", function (response) {
        console.log(response);
    });

    // 演示POST请求
    Ajax.post("users.json", "", function (response) {
        console.log(response);
    });

#### Cookie ####
##### Cookie概述 #####
Cookie 是一些数据，存储于你电脑上的文本文件中，当 web 服务器向浏览器发送 web 页面时，在连接关闭后，服务端不会记录用户的信息，Cookie 的作用就是用于解决 “如何记录客户端的用户信息”：

当用户访问 web 页面时，它的名字可以记录在 cookie 中。
在用户下一次访问该页面时，可以在 cookie 中读取用户访问记录。
Cookie 以名/值对形式存储，如下所示：

username=zhangsan
1
当浏览器从服务器上请求 web 页面时， 属于该页面的 cookie 会被添加到该请求中，服务端通过这种方式来获取用户的信息。

JavaScript 可以使用 document.cookie 属性来创建 、读取、及删除 Cookie。

##### Cookie创建 #####
JavaScript 中，创建 cookie 如下所示：

document.cookie = "username=zhangsan";
您还可以为 cookie 添加一个过期时间（以 UTC 或 GMT 时间）。默认情况下，cookie 在浏览器关闭时删除。

document.cookie = "username=zhangsan; expires=Thu, 18 Dec 2043 12:00:00 GMT";
您可以使用 path 参数告诉浏览器 cookie 的路径。默认情况下，cookie 属于当前页面。

document.cookie = "username=zhangsan; expires=Thu, 18 Dec 2043 12:00:00 GMT; path=/";
##### Cookie读取 #####
JavaScript 中，读取 cookie 如下所示：

document.cookie 将以字符串的方式返回所有的 cookie，类型格式： cookie1=value; cookie2=value; cookie3=value;

document.cookie = "username=zhangsan";
var cookies = document.cookie;

##### Cookie修改 #####

使用 document.cookie 将旧的 cookie 将被覆盖就是修改。

document.cookie = "username=zhangsan";
document.cookie = "username=lisi";
var cookies = document.cookie;

##### Cookie删除 #####
JavaScript 中，删除 cookie 如下所示：

删除 cookie 非常简单，您只需要设置 expires 参数为以前的时间即可，如下所示，设置为 Thu, 01 Jan 1970 00:00:00 GMT:

document.cookie = "username=zhangsan";
document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
var cookies = document.cookie;

##### Cookie值设置函数 #####
    /**
    * Cookie值设置函数
    * @param cname     cookie名称
    * @param cvalue    cookie值
    * @param exdays    过期天数
    */
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toGMTString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    }

##### Cookie值获取函数 #####
    /**
    * Cookie值获取函数
    * @param cname     cookie名称
    * @returns {string}
    */
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i].trim();
            if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
        }
        return "";
    }
#### WebStorage ####
##### WebStorage概述 #####
WebStorage是HTML5中本地存储的解决方案之一，在HTML5的WebStorage概念引入之前除去IE User Data、Flash Cookie、Google Gears等看名字就不靠谱的解决方案，浏览器兼容的本地存储方案只有使用Cookie。有同学可能会问，既然有了Cookie本地存储，为什么还要引入WebStorage的概念？那就要说一说Cookie的缺陷了：

数据大小：作为存储容器，Cookie的大小限制在4KB左右这是非常坑爹的，尤其对于现在复杂的业务逻辑需求，4KB的容量除了存储一些配置字段还简单单值信息，对于绝大部分开发者来说真的不知指望什么了。
安全性问题：由于在HTTP请求中的Cookie是明文传递的（HTTPS不是），带来的安全性问题还是很大的。
网络负担：我们知道Cookie会被附加在每个HTTP请求中，在HttpRequest和HttpResponse的header中都是要被传输的，所以无形中增加了一些不必要的流量损失。
虽然WebStorage是HTML5新增的本地存储解决方案之一，但并不是为了取代Cookie而制定的标准，Cookie作为HTTP协议的一部分用来处理客户端和服务器通信是不可或缺的，session正是依赖于实现的客户端状态保持。WebStorage的意图在于解决本来不应该Cookie做，却不得不用Cookie的本地存储的应用场景。

##### WebStorage分类 #####
Web Storage又分为两种： sessionStorage 和localStorage ，即这两个是Storage的一个实例。从字面意思就可以很清楚的看出来，sessionStorage将数据保存在session中，浏览器关闭也就没了；而localStorage则一直将数据保存在客户端本地； 不管是sessionStorage，还是localStorage，使用的API都相同。

localStorage和sessionStorage只能存储字符串类型，对于复杂的对象可以使用ECMAScript提供的JSON对象的stringify和parse来处理，低版本IE可以使用json2.js

##### localStorage方法 #####
对象介绍：

localStorage在本地永久性存储数据，除非显式将其删除或清空。

* 保存单个数据：localStorage.setItem(key,value);
* 读取单个数据：localStorage.getItem(key);
* 删除单个数据：localStorage.removeItem(key);
* 删除所有数据：localStorage.clear();
* 获取某个索引的key：localStorage.key(index);


##### sessionStorage方法 #####

sessionStorage对象存储特定于某个对话的数据，也就是它的生命周期为当前窗口或标签页，一旦窗口或标签页被永久关闭了，那么所有通过sessionStorage存储的数据也就被清空了。存储在sessionStorage中的数据可以跨越页面刷新而存在，同时如果浏览器支持，浏览器崩溃并重启之后依然可以使用（注意：Firefox和Weblit都支持，IE则不行）。

因为sessionStorage对象绑定于某个服务器会话，所以当文件在本地运行的时候是不可用的。存储在sessionStorage中的数据只能由最初给对象存储数据的页面访问到，所以对多页面应用有限制。

不同浏览器写入数据方法略有不同。Firefox和Webkit实现了同步写入，所以添加到存储空间中的数据是立刻被提交的。而IE的实现则是异步写入数据，所以在设置数据和将数据实际写入磁盘之间可能有一些延迟。

常见方法：

* 保存单个数据：sessionStorage.setItem(key,value);
* 读取单个数据：sessionStorage.getItem(key);
* 删除单个数据：sessionStorage.removeItem(key);
* 删除所有数据：sessionStorage.clear();
* 获取某个索引的key：sessionStorage.key(index);

#### Closure

需求信息：点击某个按钮，提示"点击的是第n个按钮"

1. 将btn所对应的下标保存在btn上
```
var btns = document.getElementsByTagName('button');

//将btn所对应的下标保存在btn上
for (var i = 0, length = btns.length; i < length; i++) {
    var btn = btns[i];
    btn.index = i;
    btn.onclick = function () {
        alert('第' + (this.index + 1) + '个');
    }
```
2. 利用闭包延长局部变量的生命周期
```
var btns = document.getElementsByTagName('button');

// 利用闭包延长局部变量的生命周期
for (var i = 0, length = btns.length; i < length; i++) {
    (function (j) {
        var btn = btns[j];
        btn.onclick = function () {
            alert('第' + (j + 1) + '个');
        }
    })(i);
}
```

##### 闭包概念 #####
1. 如何产生闭包?
当一个嵌套的内部(子)函数引用了嵌套的外部(父)函数的变量(函数)时，就产生了闭包
2. 什么才是闭包？
理解一：闭包是嵌套的内部函数(绝大部分人认为)
它的最大用处有两个，一个是可以读取函数内部的变量，另一个就是让这些变量的值始终保持在内存中


##### 闭包生命周期 #####
生命周期：

* 产生：在嵌套内部函数定义执行完时就产生了(不是在调用)
* 死亡：在嵌套的内部函数成为垃圾对象时就死亡了

```
function fn1() {
    //此时闭包就已经产生了(函数提升, 内部函数对象已经创建了)
    var a = 2;

    function fn2() {
        a++;
        console.log(a);
    }

    return fn2;
}

var f = fn1();
f(); // 3
f(); // 4
f = null; //闭包死亡(包含闭包的函数对象成为垃圾对象)
```

##### 闭包应用 #####

具有特定功能的js文件
将所有的数据和功能都封装在一个函数内部(私有的)
只向外暴露一个包含n个方法的对象或函数
模块的使用者，只需要通过模块暴露的对象调用方法来实现对应的功能.

    function myModule() {
        //私有数据
        var msg = 'Hello, World';

        //操作数据的函数
        function doSomething() {
            console.log('doSomething() ' + msg.toUpperCase());
        }

        function doOtherthing() {
            console.log('doOtherthing() ' + msg.toLowerCase());
        }

        //向外暴露对象(给外部使用的方法)
        return {
            doSomething: doSomething,
            doOtherthing: doOtherthing
        }
    }

第二种格式：myModule.js

    (function (window) {
        //私有数据
        var msg = 'Hello, World';

        //操作数据的函数
        function doSomething() {
            console.log('doSomething() ' + msg.toUpperCase());
        }

        function doOtherthing() {
            console.log('doOtherthing() ' + msg.toLowerCase());
        }

        //向外暴露对象(给外部使用的方法)
        window.myModule = {
            doSomething: doSomething,
            doOtherthing: doOtherthing
        }
    })(window);

## JavaScript新特性 ##
### ECMAScript6新特性 ###
##### let 关键字 #####
let 关键字用来声明变量，使用 let 声明的变量有几个特点：

* 不允许重复声明
* 块儿级作用域
* 不存在变量提升
* 不影响作用域链
注意：以后声明变量使用 let 就对了


##### const 关键字 ####
const 关键字用来声明常量，const 声明有以下特点：

* 不允许重复声明
* 块儿级作用域
* 声明必须赋初始值
* 值不允许修改
* 标识符一般为大写
注意：声明对象类型使用 const，非对象类型声明选择 let
##### 变量的解构赋值 #####
ES6 允许按照一定模式，从数组和对象中提取值，对变量进行赋值，这被称为解构赋值。
注意：频繁使用对象方法、数组元素，就可以使用解构赋值形式


    //数组的解构赋值
    const arr = ["张学友", "刘德华", "黎明", "郭富城"];
    let [zhang, liu, li, guo] = arr;

    //复杂对象的解构赋值
    let wangfei = {
        name: "王菲",
        age: 18,
        songs: ["红豆", "流年", "暧昧"],
        history: [
            {name: "窦唯"},
            {name: "李亚鹏"},
            {name: "谢霆锋"}
        ]
    };

##### 模板字符串 #####
模板字符串（template string）是增强版的字符串，用反引号（`）标识，特点：

* 字符串中可以出现换行符
* 可以使用 ${xxx} 形式输出变量
注意：当遇到字符串与变量拼接的情况使用模板字符串

    let name = '小可爱';
    let result = `欢迎${name}访问我的文章`;

image-20201025153746643

##### 简化对象写法 #####
ES6 允许在大括号里面，直接写入变量和函数，作为对象的属性和方法，这样的书写更加简洁。

注意：对象简写形式简化了代码，所以以后用简写就对了

    let name = "张三";
    let age = 18;
    let speak = function () {
        console.log(this.name);
    };

    //属性和方法简写
    let person = {
        name,
        age,
        speak
    };

##### 箭头函数 #####
ES6 允许使用「箭头」（=>）定义函数，通用写法如下：

let fn = (arg1, arg2, arg3) => {
    return arg1 + arg2 + arg3;
}

箭头函数的注意点：

* 如果形参只有一个，则小括号可以省略
* 函数体如果只有一条语句，则花括号可以省略，函数的返回值为该条语句的执行结果
* 箭头函数 this 指向声明时所在作用域下 this 的值，箭头函数不会更改 this 指向，用来指定回调函数会非常合适
* 箭头函数不能作为构造函数实例化
* 不能使用 arguments 实参

##### rest 参数 #####
ES6 引入 rest 参数，用于获取函数的实参，用来代替 arguments 参数。
注意：rest 参数非常适合不定个数参数函数的场景

    // 作用与 arguments 类似
    function add(...args) {
        console.log(args);
    }
    add(1, 2, 3, 4, 5);

    // rest 参数必须是最后一个形参
    function minus(a, b, ...args) {
        console.log(a, b, args);
    }
    minus(100, 1, 2, 3, 4, 5, 19);

##### spread 扩展运算符 #####
扩展运算符（spread）也是三个点（…），它好比 rest 参数的逆运算，将一个数组转为用逗号分隔的参数序列，对数组进行解包。

    // 展开数组
    let tfboys = ["德玛西亚之力", "德玛西亚之翼", "德玛西亚皇子"];
    function fn() {
        console.log(arguments);
    }
    fn(...tfboys);


##### Symbol类型 #####
###### Symbol的使用 ######
ES6 引入了一种新的原始数据类型 Symbol，表示独一无二的值，它是 JavaScript 语言的第七种数据类型，是一种类似于字符串的数据类型，Symbol 特点如下：

Symbol 的值是唯一的，用来解决命名冲突的问题
Symbol 值不能与其它数据进行运算
Symbol 定义的对象属性不能使用 for…in 循环遍 历 ，但是可以使用 Reflect.ownKeys 来获取对象的所有键名
    //创建 Symbol
    let s1 = Symbol();
    console.log(s1);
    console.log(typeof s1);

    //添加标识的 Symbol
    let s2 = Symbol("张三");
    let s2_2 = Symbol("张三");
    console.log(s2);
    console.log(s2_2);
    console.log(s2 === s2_2);

    //使用 Symbol for 定义
    let s3 = Symbol.for("张三");
    let s3_2 = Symbol.for("张三");
    console.log(s3);
    console.log(s3_2);
    console.log(s3 === s3_2);

    //在方法中使用 Symbol
    let game = {
        name: "狼人杀",
        [Symbol('say')]: function () {
            console.log("我可以发言")
        },
        [Symbol('zibao')]: function () {
            console.log('我可以自爆');
        }
    };


###### Symbol内置值 ######
除了定义自己使用的 Symbol 值以外，ES6 还提供了 11 个内置的 Symbol 值，指向语言内部使用的方法。

可以称这些方法为魔术方法，因为它们会在特定的场景下自动执行。

* Symbol.hasInstance	当其它对象使用 instanceof 运算符，判断是否为该对象的实例时，会调用这个方法
* Symbol.isConcatSpreadable	对象的 Symbol.isConcatSpreadable 属性等于的是一个布尔值，表示该对象用于 Array.prototype.concat()时， 是否可以展开
* Symbol.species	创建衍生对象时，会使用该属性
* Symbol.match	当执行 str.match(myObject) 时，如果该属性存在，会调用它，返回该方法的返回值
* Symbol.replace	当该对象被 str.replace(myObject)方法调用时，会返回该方法的返回值
* Symbol.search	当该对象被 str.search (myObject)方法调用时，会返回该方法的返回值
* Symbol.split	当该对象被 str.split(myObject)方法调用时，会返回该方法的返回值
* Symbol.iterator	当对象进行 for…of 循环时，会调用 Symbol.iterator 方法， 返回该对象的默认遍历器
* Symbol.toPrimitive	当对象被转为原始类型的值时，会调用这个方法，返 回该对象对应的原始类型值
* Symbol. toStringTag	当对象上面调用 toString 方法时，返回该方法的返 回值
* Symbol. unscopables	当对象指定了使用 with 关键字时，哪些属性会被 with 环境排除
* Symbol.hasInstance演示：

#### 迭代器 ####
遍历器（Iterator）就是一种机制。它是一种接口，为各种不同的数据结构提供统一的访问机制。任何数据结构只要部署 Iterator 接口，就可以完成遍历操作。ES6 创造了一种新的遍历命令 for…of 循环，Iterator 接口主要供 for…of 消费，原生具备 iterator 接口的数据：

* Array
* Arguments
* Set
* Map
* String
* TypedArray
* NodeList

工作原理：

> 创建一个指针对象，指向当前数据结构的起始位置.第一次调用对象的 next 方法，指针自动指向数据结构的第一个成员.接下来不断调用 next 方法，指针一直往后移动，直到指向最后一个成员.每调用 next 方法返回一个包含 value 和 done 属性的对象
案例演示：遍历数组

    //声明一个数组
    const xiyou = ["唐僧", "孙悟空", "猪八戒", "沙僧"];
    //使用 for...of 遍历数组
    for (let v of xiyou) {
        console.log(v);
    }

//获取迭代器对象
let iterator = xiyou\[Symbol.iterator]();
//调用对象的next方法
console.log(iterator.next());
console.log(iterator.next());
console.log(iterator.next());
console.log(iterator.next());
console.log(iterator.next());

    //声明一个对象
    const banji = {
        name: "五班",
        stus: [
            "张三",
            "李四",
            "王五",
            "小六"
        ],
        [Symbol.iterator]() {
            //索引变量
            let index = 0;
            let _this = this;
            return {
                next: function () {
                    if (index < _this.stus.length) {
                        const result = {value: _this.stus[index], done: false};
                        //下标自增
                        index++;
                        //返回结果
                        return result;
                    } else {
                        return {value: undefined, done: true};
                    }
                }
            };
        }
    }
#### 生成器 ####
生成器函数是 ES6 提供的一种异步编程解决方案，语法行为与传统函数完全不同。

7.1.11.1、生成器函数使用
代码说明：

\* 的位置没有限制
生成器函数返回的结果是迭代器对象，调用迭代器对象的 next 方法可以得到 yield 语句后的值
yield 相当于函数的暂停标记，也可以认为是函数的分隔符，每调用一次 next 方法，执行一段代码
next 方法可以传递实参，作为 yield 语句的返回值
function * gen() {
    /*代码1开始执行*/
    console.log("代码1执行了");
    yield "一只没有耳朵";
    /*代码2开始执行*/
    console.log("代码2执行了");
    yield "一只没有尾巴";
    /*代码3开始执行*/
    console.log("代码3执行了");
    return "真奇怪";
}

let iterator = gen();
console.log(iterator.next());
console.log(iterator.next());
console.log(iterator.next());


##### 生成器函数参数 #####
function * gen(arg) {
    console.log(arg);
    let one = yield 111;
    console.log(one);
    let two = yield 222;
    console.log(two);
    let three = yield 333;
    console.log(three);
}

//执行获取迭代器对象
let iterator = gen('AAA');
console.log(iterator.next());

//next方法可以传入实参
console.log(iterator.next('BBB'));
console.log(iterator.next('CCC'));
console.log(iterator.next('DDD'));


#### Promise ####
Promise 是 ES6 引入的异步编程的新解决方案，语法上 Promise 是一个构造函数，用来封装异步操作并可以获取其成功或失败的结果。

##### Promise基本使用 #####
    //实例化 Promise 对象
    const p = new Promise(function (resolve, reject) {
        setTimeout(function () {

            // 成功调用resolve()处理
            let data = "数据读取成功";
            resolve(data);

            // 失败调用reject()处理
            let err = "数据读取失败";
            reject(err);

        }, 1000);
    });

    //调用 promise 对象的 then 方法
    p.then(function (value) {
        console.log(value);
    }, function (reason) {
        console.error(reason);
    });
##### Promise案例演示 #####

    // 接口地址: https://api.apiopen.top/getJoke
    const p = new Promise((resolve, reject) => {
        //1. 创建对象
        const xhr = new XMLHttpRequest();
        //2. 初始化
        xhr.open("GET", "https://api.apiopen.top/getJoke");
        //3. 发送
        xhr.send();
        //4. 绑定事件, 处理响应结果
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                //判断响应状态码 200-299
                if (xhr.status >= 200 && xhr.status < 300) {
                    //表示成功
                    resolve(xhr.response);
                } else {
                    //如果失败
                    reject(xhr.status);
                }
            }
        }
    });

    //指定回调
    p.then(function (value) {
        console.log(value);
    }, function (reason) {
        console.error(reason);
    });
##### Promise-then方法 #####
调用 then 方法，then 方法的返回结果是 Promise 对象，对象状态由回调函数的执行结果决定，如果回调函数中返回的结果是 非 promise 类型的属性，状态为成功，返回值为对象的成功的值

    //创建 promise 对象
    const p = new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve("用户数据");
        }, 1000)
    });

    //链式调用+箭头函数
    p.then(value => {
        console.log(value);
        return value;
    }).then(value => {
        console.log(value);
    });


##### Promise-catch方法 #####
如果只想处理错误状态，我们可以使用 catch 方法

    const p = new Promise((resolve, reject) => {
        setTimeout(() => {
            //设置 p 对象的状态为失败, 并设置失败的值
            reject("出错啦!");
        }, 1000);
    });

    p.catch(function (reason) {
        console.error(reason);
    });


#### Set ####
ES6 提供了新的数据结构 Set（集合）。它类似于数组，但成员的值都是唯一的，集合实现了 iterator 接口，所以可以使用『扩展运算符』和『for…of…』进行遍历，集合的属性和方法：

* size：返回集合的元素个数
* add()：增加一个新元素，返回当前集合
* delete()：删除元素，返回 boolean 值
* has()：检测集合中是否包含某个元素，返回 boolean 值
* clear()：清空集合，返回 undefined
```
    let s = new Set(); //创建一个空集合
    let s1 = new Set([1, 2, 3, 1, 2, 3]); //创建一个非空集合
```

#### Map ####
ES6 提供了 Map 数据结构。它类似于对象，也是键值对的集合。但是“键” 的范围不限于字符串，各种类型的值（包括对象）都可以当作键。Map 也实现了 iterator 接口，所以可以使用『扩展运算符』和『for…of…』进行遍历。Map 的属性和方法：

* size：返回 Map 的元素个数
* set()：增加一个新元素，返回当前 Map
* get()：返回键名对象的键值
* has()：检测 Map 中是否包含某个元素，返回 boolean 值
* clear()：清空集合，返回 undefined
```
let m = new Map(); //创建一个空 map
let m2 = new Map([
    ["name", "张三"],
    ["gender", "女"]
]); //创建一个非空 map
```


#### class 类 ####
ES6 提供了更接近传统语言的写法，引入了 Class（类）这个概念，作为对象的模板。通过 class 关键字，可以定义类。基本上，ES6 的 class 可以看作只是 一个语法糖，它的绝大部分功能，ES5 都可以做到，新的 class 写法只是让对象原型的写法更加清晰、更像面向对象编程的语法而已，它的一些如下：

* class：声明类
* constructor：定义构造函数初始化
* extends：继承父类
* super：调用父级构造方法
* static：定义静态方法和属性
```  
//父类
class Phone {
    //构造方法
    constructor(brand, color, price) {
        this.brand = brand;
        this.color = color;
        this.price = price;
    }

    //对象方法
    call() {
        console.log("我可以打电话!!!")
    }
}
```
```
//子类
class SmartPhone extends Phone {
    constructor(brand, color, price, screen, pixel) {
        super(brand, color, price);
        this.screen = screen;
        this.pixel = pixel;
    }

    //子类方法
    photo() {
        console.log("我可以拍照!!");
    }

    playGame() {
        console.log("我可以玩游戏!!");
    }

    //方法重写
    call() {
        console.log("我可以进行视频通话!!");
    }

    //静态方法
    static run() {
        console.log("我可以运行程序")
    }

    static connect() {
        console.log("我可以建立连接")
    }
}
```

12
13
14
15
16
image-20201026085337223

JSON.parse(JSON.stringify(obj))：可实现多维对象的深拷贝，但会忽略 undefined 、 任意的函数 、Symbol 值

var obj1 = {
    name: "张三",
    age: 20,
    birthday: {
        year: 1997,
        month: 12,
        day: 5
    },
    speak: function () {
        console.log("我是" + this.name);
    }
};

var obj2 = JSON.parse(JSON.stringify(obj1));

// 当修改obj2的属性和方法的时候，obj1相应的属性和方法不会改变
obj2.name = "李四";
console.log(obj1);
console.log(obj2);
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
image-20201026085639830

注意：进行JSON.stringify()序列化的过程中，undefined、任意的函数以及 symbol 值，在序列化过程中会被忽略（出现在非数组对象的属性值中时）或者被转换成 null（出现在数组中时），由上面可知，JS 提供的自有方法并不能彻底解决Array、Object的深拷贝问题，因此我们应该自己实现。

7.1.19.2.2、通用版
var obj1 = {
    name: "张三",
    age: 20,
    birthday: {
        year: 1997,
        month: 12,
        day: 5
    },
    speak: function () {
        console.log("我是" + this.name);
    }
};

var obj2 = deepClone(obj1);

// 当修改obj2的属性和方法的时候，obj1相应的属性和方法不会改变
obj2.name = "李四";
console.log(obj1);
console.log(obj2);

/**
 * 深拷贝通用方法
 * @param obj   需要拷贝的对象
 * @param has
 * @returns {any|RegExp|Date}
 */
function deepClone(obj, has = new WeakMap()) {
    // 类型检查
    if (obj == null) return obj;
    if (obj instanceof Date) return obj;
    if (obj instanceof RegExp) return obj;
    if (!(typeof obj == "object")) return obj;

    // 构造对象
    const newObj = new obj.constructor;

    // 防止自引用导致的死循环
    if (has.get(obj)) return has.get(obj);
    has.set(obj, newObj);

    // 循环遍历属性及方法
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            newObj[key] = deepClone(obj[key]);
        }
    }

    // 返回对象
    return newObj;
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
image-20201026090711359

#### ECMAScript7新特性 ####

Array.prototype.includes：此方法用来检测数组中是否包含某个元素，返回布尔类型值

    const mingzhu = ["西游记", "红楼梦", "三国演义", "水浒传"];
    console.log(mingzhu.includes("西游记"));


###### 幂运算 ######
** 操作符的作用和 Math.pow 的作用是一样，请看代码：

console.log(2 ** 10);
console.log(Math.pow(2, 10));

#### ECMAScript8新特性 ####
##### async 函数 #####
async 函数的语法：

async function fn(){
    
}

async 函数的返回值：

返回的结果不是一个 Promise 类型的对象，返回的结果就是成功 Promise 对象
返回的结果如果是一个 Promise 对象，具体需要看执行resolve方法还是reject方法
抛出错误，返回的结果是一个失败的 Promise
async 函数的演示：

    //async 函数
    async function fn() {
        return new Promise((resolve, reject) => {
            resolve('成功的数据');
            // reject("失败的错误");
        });
    }

    const result = fn();

    //调用 then 方法
    result.then(value => {
        console.log(value);
    }, reason => {
        console.warn(reason);
    });
    1
    2
    3

##### await 表达式 #####
async 和 await 两种语法结合可以让异步代码像同步代码一样

await 表达式的注意事项：

* await 必须写在 async 函数中
* await 右侧的表达式一般为 promise 对象
* await 返回的是 promise 成功的值
* await 的 promise 失败了, 就会抛出异常, 需要通过 try…catch 捕获处理
* await 表达式的语法演示：

    //创建 promise 对象
    const p = new Promise((resolve, reject) => {
        resolve("用户数据");
        //reject("失败啦!");
    })

    //await 要放在 async 函数中.
    async function fun() {
        try {
            let result = await p;
            console.log(result);
        } catch (e) {
            console.log(e);
        }
    }

> await 表达式的案例演示：async与await封装AJAX请求

    // 发送 AJAX 请求, 返回的结果是 Promise 对象
    function sendAJAX(url) {
        return new Promise((resolve, reject) => {
            //1. 创建对象
            const x = new XMLHttpRequest();
            //2. 初始化
            x.open('GET', url);
            //3. 发送
            x.send();
            //4. 事件绑定
            x.onreadystatechange = function () {
                if (x.readyState === 4) {
                    if (x.status >= 200 && x.status < 300) {
                        resolve(x.response);//成功
                    } else {
                        reject(x.status);//失败
                    }
                }
            }
        })
    }


    // async 与 await 测试
    async function fun() {
        //发送 AJAX 请求 1
        let joke = await sendAJAX("https://api.apiopen.top/getJoke");
        //发送 AJAX 请求 2
        let tianqi = await sendAJAX('https://www.tianqiapi.com/api/?version=v1&city=%E5%8C%97%E4%BA%AC&appid=23941491&appsecret=TXoD5e8P')

        console.log(joke);
        console.error(tianqi);//为了区别数据，我这里用红色的error输出
    }


#### 对象方法拓展 ####
* Object.keys()方法返回一个给定对象的所有可枚举键值的数组
* Object.values()方法返回一个给定对象的所有可枚举属性值的数组
* Object.entries()方法返回一个给定对象自身可遍历属性 [key,value] 的数组

```
//获取对象所有的键
console.log(Object.keys(person));
//获取对象所有的值
console.log(Object.values(person));
//获取对象所有的键值对数组
console.log(Object.entries(person));
//创建 Map
const m = new Map(Object.entries(person));
console.log(m.get("name"));
```
* Object.getOwnPropertyDescriptors方法返回指定对象所有自身属性的描述对象
```
//声明对象
const person = {
    name: "张三",
    age: 20
};
//对象属性的描述对象
console.log(Object.getOwnPropertyDescriptors(person));
```
```
//声明对象
const obj = Object.create(null, {
    name: {
        //设置值
        value: "李四",
        //属性特性
        writable: true,
        configurable: true,
        enumerable: true
    },
    age: {
        //设置值
        value: 21,
        //属性特性
        writable: true,
        configurable: true,
        enumerable: true
    }
});
//对象属性的描述对象
console.log(Object.getOwnPropertyDescriptors(obj));
```


##### 正则表达式拓展 #####
###### 命名捕获分组 ######
ES9 允许命名捕获组使用符号 ?<name> ，这样获取捕获结果可读性更强。使用数组下标不好吗？的确不好，因为如果一旦你想要获取的元素一旦增加，数组下标就改变了，所以建议使用命名捕获分组

    let str = '<a href="https://www.baidu.com">打开百度，你就知道！</a>';
    const reg = /<a href="(?<url>.*)">(?<text>.*)<\/a>/;
    const result = reg.exec(str);
    console.log(result.groups.url);
    console.log(result.groups.text);


###### 正向断言 ######
ES9 支持正向断言，通过对匹配结果后面的内容进行判断，对匹配进行筛选。

    //声明字符串
    let str = "订单编号开始123456789订单编号结束";
    //正向断言
    const reg = /\d+(?=订单编号结束)/;//也就是说数字的后边一定要跟着 订单编号结束
    const result = reg.exec(str);
    console.log(result);


###### 反向断言 ######
ES9 支持反向断言，通过对匹配结果前面的内容进行判断，对匹配进行筛选。

    //声明字符串
    let str = "订单编号开始123456789订单编号结束";
    //正向断言
    const reg = /(?<=订单编号开始)\d+/;//也就是说数字的前边一定要跟着 订单编号开始
    const result = reg.exec(str);
    console.log(result);


###### dotAll模式 ######
正则表达式中点 . 匹配除回车外的任何单字符，标记 s 改变这种行为，允许行终止符出现，也就是dotAll模式

    let str = `
    <ul>
        <li>
            <a>肖生克的救赎</a>
            <p>上映日期: 1994-09-10</p>
            </li>
        <li>
            <a>阿甘正传</a>
            <p>上映日期: 1994-07-06</p>
        </li>
    </ul>`;

    //声明正则
    const reg = /<li>.*?<a>(.*?)<\/a>.*?<p>(.*?)<\/p>/gs;

    // 执行匹配
    let result;
    let data = [];
    while (result = reg.exec(str)) {
        data.push({title: result[1], time: result[2]});
    }

###### 字符串方法拓展 ######
let str = "   iloveyou   ";
console.log(str.trimStart());//只去除前边的空格
console.log(str.trimEnd());//只去除后边的空格


###### 数组方法拓展 ######
flat() 方法会按照一个可指定的深度递归遍历数组，并将所有元素与遍历到的子数组中的元素合并为一个新数组返回，说白了就是将多维数组转化为低维数组。

    const arr1 = [1, 2, 3, 4, [5, 6]];
    console.log(arr1.flat());
    const arr2 = [1, 2, 3, 4, [5, 6, [7, 8, 9]]];
    console.log(arr2.flat());
    console.log(arr2.flat(1));//参数为深度是一个数字
    console.log(arr2.flat(2));//参数为深度是一个数字

flatMap() 方法首先使用映射函数映射每个元素，然后将结果压缩成一个新数组。它与 map 连着深度值为1的 flat 几乎相同，但 flatMap 通常在合并成一种方法的效率稍微高一些。

    var arr1 = [1, 2, 3, 4];
    console.log(arr1.map(x => x * 2));

    var arr2 = [1, 2, 3, 4];
    console.log(arr2.flatMap(x => x * 2));


###### 字符串方法扩展 ###### <a name="字符串方法扩展"></a>
String.prototype.matchAll() 方法返回一个包含所有匹配正则表达式的结果及分组捕获组的迭代器。

    let str =
    `<ul>
        <li>
            <a>肖生克的救赎</a>
            <p>上映日期: 1994-09-10</p>
        </li>
        <li>
            <a>阿甘正传</a>
            <p>上映日期: 1994-07-06</p>
        </li>
    </ul>`;

    //声明正则
    const reg = /<li>.*?<a>(.*?)<\/a>.*?<p>(.*?)<\/p>/sg;

    //调用方法
    const result = str.matchAll(reg);
    for (let v of result) {
        console.log(v);

