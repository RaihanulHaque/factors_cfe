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
            return f"No. The square root of 10365 isn’t an integer. So it isn’t a square number."

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
        title = f"Prime Factorization of {self.n}: Division, Factor Tree Methods"
        return title

    def prepareIntro(self):
        p1 = self.wp_paragraph(
            f"{self.multi_primef} = {self.n}. So, the prime factors of {self.n} are {self.unique_primef(self.n)}.")
        p2 = self.wp_paragraph(
            f"If you multiply the prime numbers {self.str_primef}, you will obtain {self.n}. The prime factors of {self.n} are therefore {self.unique_primef(self.n)}.")
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

        h = self.wp_h2("Prime Factors by Definition")
        post += h

        p = self.wp_paragraph("We should become familiar with the term \"prime factors\" before learning how to calculate them. What are prime factors? Why are they known as prime factors? A product's factors can be thought of as the multipliers of that product. And they can be referred to as prime factors if the multipliers are prime values. However, remember that a factor cannot be a fractional number. Therefore, only whole numbers may be used as multipliers. So, we can say, a number's factors are referred to be prime factors if they are prime numbers.")
        post += p

        c = self.wp_paragraph_center("105 = 3 x 5 x 7")
        post += c

        p = self.wp_paragraph(
            "Here, 105 is the product of multiplication of 3, 5, 7. All the multipliers are prime numbers. So, 3, 5, 7 are the prime factors of 105.")
        post += p

        h = self.wp_h2("What is Factorization?")
        post += h

        p = self.wp_paragraph(
            "Finding all the integers that divide a given number perfectly is a technique known as factorization. We can calculate all those factors using various techniques. But keep in mind that both the provided number and the divisors must be integers.")
        post += p

        h = self.wp_h2("What is Prime Factorization?")
        post += h

        p = self.wp_paragraph(
            "Prime factorization is the technique of identifying prime factors.")
        post += p

        return post

    def prepareFormula(self):
        post = ""

        post += self.wp_h2("Formula of Prime Factor")
        post += self.wp_paragraph("A prime factor must be both a factor of the supplied number and a prime number. Basically, by decomposing the provided number, prime factors can be found. Generally, we show our supplied number as the result of prime numbers combined with their respective orders. These prime numbers are definitely the given number's prime factors. Mathematical expression for prime factors:")
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
            f"How to Find the Prime Factors of {self.n}?")
        post += self.wp_paragraph(
            "Prime factors can be found in several ways. Two of the most common methods are::")
        post += f"<!-- wp:list --><ul><li>Factor Tree Method. </li><li>Division Method.</li></ul><!-- /wp:list -->"
        return post

    def prepareFactorTree(self):
        post = ""
        post += self.wp_h3("Factor Tree Method")

        p1 = self.wp_paragraph(
            "Factor tree method, which mostly relies on diagrams. This term was chosen because the diagram produced by the factor tree method resembles a tree. The base of the tree is the supplied integer, and the branches are the factors which are graphically linked using diagonals.")
        post += p1

        image = self.image_add_tree()
        post += image

        p2 = self.wp_paragraph(
            "The top of each branch in this technique is where the prime factors are located. We can execute it by dividing it into small steps.")
        post += p2

        return post

    def prepareDivision(self):
        post = ""
        post += self.wp_h3("Division Method")

        p1 = self.wp_paragraph(
            "We will now discuss the division method. We can guess that this approach is connected to division operation from the name. This technique is actually quite easy to use. Simply keep dividing the given number until the quotient equals one.")

        image = self.image_add_division()

        p2 = self.wp_paragraph(
            f"Let's go over the specifics of this procedure using the given number {self.n}.")

        post += p1 + image + p2
        return post

    def prepareExtra1(self):
        post = ""
        positive_factors, positive_non_prime_factors, negative_factors, division_code, multiply_code = self.extraPrimeF(
            self.n)

        # closestprime = self.wp_h2(
        #     f"What Is The Nearest Prime Number of {self.n}?")
        # closestprime += self.wp_paragraph(
        #     f"{self.nearestPrime(self.n)} is the nearest prime number.")
        # post += closestprime

        sec1 = self.wp_h2(f"What Are The Non-Prime Factors of {self.n}")
        sec1 += self.wp_paragraph(
            f"{positive_factors} are all positive factors of the number {self.n}. Therefore, {positive_non_prime_factors} are non-prime factors.")

        sec2 = self.wp_h2(f"What Are The Negative Factors of {self.n}")
        sec2 += self.wp_paragraph(
            f"A number also has negative factors which are rarely used. The negative factors of {self.n} are {negative_factors}.")

        sec3 = self.wp_h2(f"Find Out All the Factors of {self.n}")
        sec3 += self.wp_paragraph(
            f"To find all the factors of {self.n}, we must find every number that exactly divides it. Once we've found that, we should put it this way:")
        sec3 += division_code
        sec3 += self.wp_paragraph(
            f"Each divisor and quotient in this calculation are factors of {self.n}. <br><br>So, the positive factors of 10365 are: {positive_factors}.")
        sec3 += self.wp_paragraph(f"We can also express this like:")
        sec3 += multiply_code
        sec3 += self.wp_paragraph(
            f"So the negative factors are: {negative_factors}.<br><br>Keep in mind that we can obtain our given number only by multiplying a negative factor with another negative factor.")

        post += sec1 + sec2 + sec3

        return post

    def prepareExtra2(self):
        post = ""
        positive_factors, positive_non_prime_factors, negative_factors, division_code, multiply_code = self.extraPrimeF(
            self.n)

        sec1 = self.wp_h2(f"Some Important Facts of Factorization")
        sec1 += f"""<!-- wp:list {{\"ordered\":true}} -->
        <ol>
            <li>Fractions can't be used as factors.</li>
            <li>The given number must be an integer.</li>
            <li>Factors can be both negative & positive.</li>
            <li>Every single natural number has 1 as a component.</li>
            <li>An equation with quadratic terms can also be factored.</li>
            <li>If we divide a given number, then the divisors & the quotient of the given number are also factors of it. Example:</li>
        </ol>
        <!-- /wp:list -->"""

        sec1 += self.wp_paragraph_center(division_code)
        sec1 += self.wp_paragraph(
            f"Here, both the divisors and the quotiens {positive_factors} are the factors of {self.n}. ")

        sec2 = self.wp_h2(f"Use of Factorization in Real Life")
        sec2 += self.wp_paragraph(f"We can arrange things in a variety of ways thanks to factors. It is helpful for creating equitable divisions. In mathematics involving number theories, it has a variety of uses. Additionally, it is advantageous when comparing things, exchanging money, telling the time, etc. It is also possible to factor quadratic equations to simplify their solution.")

        post = sec1 + sec2

        return post

    def prepareFAQ(self):
        post = ""
        post += self.wp_h2("Frequently Asked Questions")

        post += self.wp_h3("1. Can Factors Be Negative?")
        post += self.wp_paragraph("Yes. Factors can be negative too. Like the factors of 10 are 1, 2, 5, 10, -1, -2, -5, -10. Because if we multiply -10 with -1, we’ll get 10. So, -10 & -1 are the factors of 10. But most of the time we use positive factors only.")

        post += self.wp_h3(f"2. Is {self.n} a Square Number?")
        post += self.wp_paragraph(self.check_squared(self.n))

        post += self.wp_h3(f"3. What Is the Square of {self.n}?")
        post += self.wp_paragraph(f"Square of {self.n} is {self.n*self.n}.")

        post += self.wp_h3(f"4. What Is the Root of {self.n}?")
        post += self.wp_paragraph(f"Root of {self.n} is {sqrt(self.n)}")

        post += self.wp_h3(
            f"5. Is {self.n} a Composite Number or a Prime Number?")
        post += self.wp_paragraph(self.isPrime_or_Composite(self.n))

        post += self.wp_h3("6. What are the factors of a prime number?")
        post += self.wp_paragraph("They are 1 & the number itself.")

        post += self.wp_h3(f"7. How Many Factors Does a Prime Number Have?")
        post += self.wp_paragraph(
            "A Prime number has only 2 factors. They are 1 & the number itself.")

        post += self.wp_h3("7. What is a Composite Number?")
        post += self.wp_paragraph(
            "If a positive integer number has more than two factors, it can be called a composite number.")

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
    # postHtml += "</html>"

    with open("view.html", "w") as htmlFile:
        htmlFile.write(postHtml)
    print(submitWP.submit(post.title, content=postHtml))
