import random
from math import floor, sqrt
import submitWP


class Post:
    def __init__(self, n):
        self.n = n
        self.primef, self.left, self.str_primef, self.multi_primef = self.primeFactors(
            n)
        self.title = self.prepareTitle()
        self.intro = self.prepareIntro()
        self.theory = self.prepareTheory()
        self.formula = self.prepareFormula()
        self.howtocalculatelist = self.howtoCalculateList()
        self.factorTree = self.prepareFactorTree()
        self.division = self.prepareDivision()
        self.extra1 = self.prepareExtra1()
        self.extra2 = self.prepareExtra2()
        self.FAQ = self.prepareFAQ()

    def primeFactors(self, n):
        c = 2
        step = 0
        str_primef = ""
        multi_primef = ""
        # expo_primef = ""
        primef = []
        left = []
        while n > 1:
            step = step + 1
            if n % c == 0:
                # print(c, end=" ")
                primef.append(c)
                left.append(int(n))
                str_primef = str_primef+f"{c}, "
                multi_primef = multi_primef + f"{c} x "
                # expo_primef = expo_primef + f"{c}<sup>1</sup> x "
                n = n / c
            else:
                c = c + 1
        left.append(1)
        return primef, left, str_primef[:-2], multi_primef[:-2]

    def unique_primef(self, n):
        unique_arr = [*set(self.primef)]
        str_unique = ""
        for x in range(0, len(unique_arr) - 1):
            str_unique += f"{unique_arr[x]}, "
        if len(unique_arr) == 1:
            str_unique = f"{str_unique[:-2]}"
        else:
            str_unique = f"{str_unique[:-2]} and {unique_arr[len(unique_arr)-1]}"
        return str_unique

    def exponential(self, array):
        frequency = {}
        str = ""
        for item in array:
            if item in frequency:
                frequency[item] += 1
            else:
                frequency[item] = 1
        for key in frequency:
            str += f"{key}<sup>{frequency[key]}</sup> x "

        return str[:-3]

    def nearestPrime(self, n):
        if (n & 1):
            n -= 2
        else:
            n -= 1
        i, j = 0, 5
        for i in range(n, 2, -2):
            if (i % 2 == 0):
                continue
            while (j <= floor(sqrt(i)) + 1):
                if (i % j == 0):
                    break
                j += 2
            if (j > floor(sqrt(i))):
                return i
        # It will only be executed when n is 3
        return 2

    def wp_h2(self, text):
        return f"<!-- wp:heading {{\"level\":2}} --><h2>{text}</h2><!-- /wp:heading -->"

    def wp_h3(self, text):
        return f"<!-- wp:heading {{\"level\":3}} --><h3>{text}</h3><!-- /wp:heading -->"

    def wp_paragraph(self, text):
        return f"<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->"

    def wp_table(self, text):
        table = f"""<!-- wp:table {{\"hasFixedLayout\":true,\"className\":\" is -style-stripes prime-factorization-table\"}} -->
        <figure class=\"wp-block-table is-style-stripes prime-factorization-table\">
        <table class=\"has-fixed-layout\">
            <tbody>
                {text}
            </tbody>
        </table>
        <figcaption>Prime Factorization of {self.n}</figcaption>
        </figure>
        <!-- /wp:table -->"""
        return table

    def wp_paragraph_center(self, text):
        return f"<!-- wp:paragraph {{\"align\":\"center\"}} --><p class = \"has-text-align-center\" >{text}</p> <!-- /wp:paragraph -->"

    def image_add_tree(self):
        locString = f"<!-- wp:image {{\"id\":452,\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"https://calculator4engineers.com/wp-content/uploads/2022/10/factor-tree-method.jpg\" alt=\"\" class=\"wp-image-452\"/></figure>"
        locString += "<!-- /wp:image -->"
        return locString

    def image_add_division(self):
        locString = f"<!-- wp:image {{\"id\":471,\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"https://calculator4engineers.com/wp-content/uploads/2022/10/division-method.jpg\" alt=\"\" class=\"wp-image-471\"/></figure>"
        locString += "<!-- /wp:image -->"
        return locString

    def check_squared(self, n):
        root = sqrt(n)
        if int(root + 0.5) ** 2 == n:
            return f"Yes. The square root of {self.n} is an integer. So it is a square number."
        else:
            return f"No. {self.n}'s square root is not an integer. Since it isn't square, it is not."

    def isPrime_or_Composite(self, n):
        # primef, left, str_primef, multi_primef = self.primeFactors(n)
        if len(self.primef) > 1:
            return f"{self.n} is a composite number."
        else:
            return f"{self.n} is a prime number."

    def extraPrimeF(self, n):
        division_code = ""
        multiply_code = ""
        holdarr = []
        holdarrstr1 = ""
        holdarrstr2 = ""

        for x in range(1, int(sqrt(n))+1):
            if n % x == 0:
                division_code += self.wp_paragraph(
                    f"{self.n} ÷ {x} = {int(n/x)}")
                multiply_code += self.wp_paragraph(f"-{int(n/x)} x -{x} = {n}")
                holdarr.append(x)
                holdarr.append(int(n/x))

        holdarr.sort()

        for y in range(0, len(holdarr)):
            holdarrstr1 = holdarrstr1 + f"{holdarr[y]}, "
            holdarrstr2 = holdarrstr2 + f"-{holdarr[y]}, "
        nonPrimefact = ""

        for x in range(0, len(self.primef)):
            if self.primef[x] in holdarr:
                holdarr.remove(self.primef[x])

        for x in range(0, len(holdarr)):
            nonPrimefact = nonPrimefact + f"{holdarr[x]}, "

        positive_factors = holdarrstr1[:-2]
        positive_non_prime_factors = nonPrimefact[:-2]
        negative_factors = holdarrstr2[:-2]

        return positive_factors, positive_non_prime_factors, negative_factors, division_code, multiply_code

    def sub(self, text):
        return f"<sub>{text}</sub>"

    def sup(self, text):
        return f"<sup>{text}</sup>"

    def strong(self, text):
        return f"<strong>{text}</strong>"

    def prepareTitle(self):
        title = f"Prime Factorization of {self.n}: Step by Step Calculation"
        return title

    def prepareIntro(self):
        p1 = self.wp_paragraph(
            f"{self.unique_primef(self.n)} are the prime factors of {self.n}.")
        p2 = self.wp_paragraph(
            f"{self.str_primef} are the prime numbers and you'll get {self.n} if you multiply {self.str_primef}. So {self.unique_primef(self.n)} are the prime factors of {self.n}.")
        intro = p1 + p2
        intro += self.wp_table(
            f"""<tr>
                    <td>Prime Factors</td><td>{self.unique_primef(self.n)}</td>
                </tr>
                <tr>
                    <td>Product of Prime Factor</td><td>{self.multi_primef}</td>
                </tr>
                <tr>
                    <td>Exponential Form</td><td>{self.exponential(self.primef)}</td>
                </tr>
                <tr>
                    <td>Total Number of Factors</td><td>{len(self.primef)}</td>
                </tr>
                <tr>
                    <td>Largest Prime Factor</td><td>{max(self.primef)}</td>
                </tr>
                <tr>
                    <td>Smallest Prime Factor</td><td>{min(self.primef)}</td>
                </tr>
                <tr>
                    <td>Closest Prime Numbers</td><td>{self.nearestPrime(self.n)}</td>
                </tr>""")
        return intro

    def prepareTheory(self):
        post = ""

        h = self.wp_h2("Introduction to Prime Factors")
        post += h

        p = self.wp_paragraph("Before learning the methods of calculating prime factors, we should get familiar with the term prime factors. What are prime factors? And why are they called prime factors? Prime factors are those integers which can express a given number as a form of their multiplication. In other words, if we multiply two prime numbers, we’ll get another number and those previous numbers are the prime factors of the later one. We’ll be more clear with an example :")
        post += p

        c = self.wp_paragraph_center("105 = 3 x 5 x 7")
        post += c

        p = self.wp_paragraph(
            "Here, the multiplication of the prime numbers 3, 5 & 7 form 105. So, 3, 5 & 7 are the prime factors of 105. From the above example, we get to know another important thing: our given number is always evenly divisible by the prime factors. As we see, 105 is evenly divisible by 3, 5 & 7. They’re being called prime factors because they are prime numbers. If they weren't prime numbers, they would’ve been called only factors.")
        post += p

        h = self.wp_h2("Definition of Factorization")
        post += h

        p = self.wp_paragraph(
            "Factorization is the process to determine all the numbers that exactly divide a given number. We can find all those numbers through different calculation methods. But remember, the given number as well as the factors must be integer numbers.")
        post += p

        h = self.wp_h2("Definition of Prime Factorization")
        post += h

        p = self.wp_paragraph(
            "Prime factorization is also a kind of factorization but the only difference is the factors are prime numbers in this case.")
        post += p

        return post

    def prepareFormula(self):
        post = ""

        post += self.wp_h2("Prime Factor's Formula")
        post += self.wp_paragraph("A prime factor must be a prime number as well as a factor of the given number. Basically, prime factors can be found by decomposing our given number. It can be expressed as a product of prime numbers with orders. In general, we represent our given number as a product of prime numbers with their orders. These prime numbers are certainly the prime factors of the given number.")
        post += self.wp_paragraph_center(
            "N = p<sub>f1</sub><sup>a1</sup> +&nbsp; p<sub>f2</sub><sup>a2</sup> +&nbsp; &nbsp; p<sub>f3</sub><sup>a3</sup> + ...... +&nbsp; p<sub>fn</sub><sup>an</sup>")

        p = "N = Any integer number<br>"
        p += "p<sub>f1</sub>, p<sub>f2</sub>, p<sub>f3</sub>, p<sub>fn</sub> = Prime factors<br>"
        p += "a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>, a<sub>n</sub> = Orders of prime factors<br>"
        p = self.wp_paragraph(p)
        post += p
        return post

    def howtoCalculateList(self):
        post = ""
        post += self.wp_h2(
            f"Methods of Calculating Prime Factors of {self.n}?")
        post += self.wp_paragraph(
            "The process of finding prime factors of a number is called prime factorization. We can determine the prime factors of 10365 in multiple ways. But here, we’ll talk about the popular methods only.")
        post += f"<!-- wp:list --><ul><li>Division Method & </li><li>Factor Tree Method.</li></ul><!-- /wp:list -->"
        return post

    def prepareFactorTree(self):
        post = ""
        post += self.wp_h3("Factor Tree Method")

        p1 = self.wp_paragraph(
            "Factor tree method, mainly a diagram based method. The reason behind this name is because  the diagram we found in the factor tree method looks like a tree. The given number is the root and prime factors are the branches of the tree. In this method, the prime factors sit at the top of every branch.")

        image = self.image_add_tree()

        p2 = self.wp_paragraph("In this case, we'll represent the supplied number as the root of a tree and its factors as their respective branches. We'll use diagonals to graphically represent the relationship between the two variables and the tree structures. We'll extract just prime factors from the tree. By breaking it down into manageable chunks, we can accomplish it.")

        post += p1 + image + p2
        return post

    def prepareDivision(self):
        post = ""
        post += self.wp_h3("Division Method")

        p1 = self.wp_paragraph(
            "Now we’ll talk about the division method. From the name, we can assume that this method is related to division operation. Actually this method is very simple. You just continue dividing the given number until the quotient becomes 1.")

        image = self.image_add_division()

        p2 = self.wp_paragraph(
            f"Let’s walk through the details of this process with a given number {self.n}.")

        post += p1 + image + p2
        return post

    def prepareExtra1(self):
        post = ""
        positive_factors, positive_non_prime_factors, negative_factors, division_code, multiply_code = self.extraPrimeF(
            self.n)
        primef, left, str_primef, multi_primef = self.primeFactors(self.n)

        # closestprime = self.wp_h2(f"Nearest prime number of {self.n}")
        # closestprime += self.wp_paragraph(
        #     f"The nearest prime number is {self.nearestPrime(self.n)}.")
        # post += closestprime

        sec1 = self.wp_h2(f"Non-Prime Factors of {self.n}")
        sec1 += self.wp_paragraph(
            f"If a given number is evenly or exactly divisible by a positive integer, then the later one is the factor of the previous one. The positive integers which exactly divide {self.n}:<br>{positive_factors}")
        sec1 += self.wp_paragraph(
            f"Those factors which aren’t prime numbers are the non-prime factors of {self.n}. They are:<br>{positive_non_prime_factors}")

        sec2 = self.wp_h2(f"Negative Factors of {self.n}")
        sec2 += self.wp_paragraph(
            f"A number has negative factors as well. We know factors basically express the given number as the product of their multiplication. In the case of {self.n}, if we multiply(-{primef[0]}) with (-{left[1]}), we’ll get {self.n}. So, it makes -{primef[0]} & -{left[1]} as the factors of {self.n}. Other negative factors of {self.n} are:<br>{negative_factors}")

        sec3 = self.wp_h2(f"Every Factors of {self.n}")
        sec3 += self.wp_paragraph(
            f"To determine all the factors of {self.n}, we have to find every divisor that divides {self.n} exactly. After finding that, we should express this like this:")
        sec3 += division_code
        sec3 += self.wp_paragraph(
            f"Here every divisor & quotient are the factors of {self.n}. <br> So, the positive factors of 10365 are: {positive_factors}.")
        sec3 += self.wp_paragraph(f"We can also express this like:")
        sec3 += multiply_code
        sec3 += self.wp_paragraph(
            f"So the negative factors are: {negative_factors}.<br><br>Remember, a negative factor must multiply with another negative factor only to get our given number.")

        post += sec1 + sec2 + sec3

        return post

    def prepareExtra2(self):
        post = ""
        positive_factors, positive_non_prime_factors, negative_factors, division_code, multiply_code = self.extraPrimeF(
            self.n)

        sec1 = self.wp_h2(f"Facts of Factorization")
        sec1 += f"""<!-- wp:list {{\"ordered\":true}} -->
        <ol>
            <li>Factors can’t be a fragment of a number.</li>
            <li>Given number must be an integer.</li>
            <li>Factors can be both negative & positive.</li>
            <li>Every single natural number has 1 as a component.</li>
            <li>A quadratic equation can also have factors.</li>
            <li>If we divide a given number, then the divisors & the quotient of the given number are also factors of it. Example:</li>
        </ol>
        <!-- /wp:list -->"""

        sec1 += self.wp_paragraph_center(division_code)
        sec1 += self.wp_paragraph(
            f"Here, both the divisors and the quotiens {positive_factors} are the factors of {self.n}. ")

        sec2 = self.wp_h2(f"Applications of Factors")
        sec2 += self.wp_paragraph(f"We can arrange things in a variety of ways thanks to factors. It is helpful for creating equitable divisions. In mathematics involving number theories, it has a variety of uses. Additionally, it is advantageous when comparing things, exchanging money, telling the time, etc. It is also possible to factor quadratic equations to simplify their solution.")

        post = sec1 + sec2

        return post

    def prepareFAQ(self):
        post = ""
        post += self.wp_h2("Most Commonly Asked Questions")

        post += self.wp_h3("1. Are There Negative Factors?")
        post += self.wp_paragraph("Yes. Factors can also be detrimental. They are 1, 2, 5, 10, -1, -2, -5, and -10, much like the factors of 10. Because we will have 10 if we multiply -10 by -1. The factors of 10 are therefore -10 and -1. However, we tend to primarily consider good factors.")

        post += self.wp_h3(f"2. Is {self.n} a Square Number?")
        post += self.wp_paragraph(self.check_squared(self.n))

        post += self.wp_h3(f"3. What Is the Square of {self.n}?")
        post += self.wp_paragraph(f"Square of {self.n} is {self.n*self.n}.")

        post += self.wp_h3(f"4. What Is the Root of {self.n}?")
        post += self.wp_paragraph(f"Root of {self.n} is {sqrt(self.n)}")

        post += self.wp_h3(
            f"5. Is {self.n} a prime or a composite number?")
        post += self.wp_paragraph(self.isPrime_or_Composite(self.n))

        post += self.wp_h3(f"6. How Many Factors Does a Prime Number Have?")
        post += self.wp_paragraph(
            "A Prime number has only 2 factors")

        post += self.wp_h3("7. What are the factors of a prime number?")
        post += self.wp_paragraph("They are 1 & the number itself.")

        post += self.wp_h3("8. What is a Composite Number?")
        post += self.wp_paragraph(
            "A positive integer number is referred to as a composite number if it has more than two elements.")

        return post


if __name__ == "__main__":

    post = Post(48)
    postHtml = ""
    # postHtml = "<html>"
    # postHtml += submitWP.title
    postHtml += post.intro
    postHtml += post.theory
    postHtml += post.howtocalculatelist
    postHtml += post.factorTree
    postHtml += post.FAQ
    # postHtml += "</html>"

    with open("view.html", "w") as htmlFile:
        htmlFile.write(postHtml)
    print(submitWP.submit(post.title, content=postHtml))
