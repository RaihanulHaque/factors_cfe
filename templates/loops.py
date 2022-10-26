import random
from math import floor, sqrt
import submitWP
import requests
import base64
import json

class FactorTreeMethod:
    def __init__(self, n, numbers, index, treeImages):
        self.n = n
        self.numbers = numbers
        self.index = index
        self.treeImages = treeImages
        # self.content = self.factorTreeSteps()

    def authenticate(self):
        user = "Rahi"
        password = "t5nC 34nz obVc BUzM c1Nt KQnK"
        creds = user + ':' + password
        cred_token = base64.b64encode(creds.encode())
        header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}
        return header

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

    def image_upload(self, path):
        header = self.authenticate()
        url = 'https://calculator4engineers.com/wp-json/wp/v2'
        media = {'file': open(path, 'rb')}
        image = requests.post(url+'/media', headers=header, files=media)
        post_id = json.loads(image.content.decode('utf-8'))['id']
        image_link = image.json()['guid']['rendered']
        locString = f"<!-- wp:image {{\"id\":{str(post_id)},\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"{image_link}\" alt=\"\" class=\"wp-image-{str(post_id)}\"/></figure>"
        locString += "<!-- /wp:image -->"
        code = locString
        # print(f"{image_link}\n")
        return code

    def link_previous(self, numbers, index):
        code = self.wp_paragraph(
            "<strong> Check the first step of these prime factorization examples to better understand how this step is done:</strong>")
        if index == 0:
            pass
        elif index == 1:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li></ul><!-- /wp:list -->"
        elif index == 2:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-2]}/\">Prime factorization of {numbers[index-2]}</a></li></ul><!-- /wp:list -->"
        else:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-2]}/\">Prime factorization of {numbers[index-2]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-3]}/\">Prime factorization of {numbers[index-3]}</a></li></ul><!-- /wp:list -->"
        return code

    def link_next(self, numbers, index):
        code = self.wp_paragraph(
            "<strong>Check the first step of these prime factorization examples to better understand how this step is done:</strong>")
        if len(numbers)-1 == index:
            pass
        elif index == len(numbers)-2:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li></ul><!-- /wp:list -->"
        elif index == len(numbers)-3:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+2]}/\">Prime factorization of {numbers[index+2]}</a></li></ul><!-- /wp:list -->"
        else:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+2]}/\">Prime factorization of {numbers[index+2]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index+3]}/\">Prime factorization of {numbers[index+3]}</a></li></ul><!-- /wp:list -->"

        return code

    def wp_h3(self, text):
        return f"<!-- wp:heading {{\"level\":3}} --><h3>{text}</h3><!-- /wp:heading -->"

    def wp_h4(self, text):
        return f"<!-- wp:heading {{\"level\":4}} --><h4>{text}</h4><!-- /wp:heading -->"

    def wp_paragraph(self, text):
        return f"<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->"

    def factorTreeSteps(self):
        n = self.n
        # index = self.index

        primef, left, str_primef, multi_primef = self.primeFactors(n)
        initialStep = []
        initialStepBy2 = []
        initialStepNotBy2 = []
        lastStep = []
        end = []
        treeImages = self.treeImages
        content = ""

######################################INITIAL STEP#########################################################################

        initialStep.append(
            f"Before we can begin to factor a given number, we need to write it down. {n} is the given number in this context. Get the first two factors of the number {n}. We'll begin with the smallest possible number, which is 2 (Note that we didn't pick 1, since every integer is divisible by both 1 and itself).<br><br>")
        initialStep.append(
            f"Let’s take {n} as our given number. Now, we’ll write the number as if it were a root of a tree. Then we’ll draw two arrows to link the root to its branches, which are actually the first two factors of the root. The first factor will be the prime number that we'll divide the root by, and the other factor will be resultant. Now, to find the prime factor of {n}, we’ll start trying from 2 and continue until we find a number that divides {n} exactly.<br><br>")
        initialStep.append(
            f"{n} is the given number whose factors are to be found. We’ll try to find its smallest factor which isn’t 1 as 1 is the divisor of every number & it isn’t a prime number. So let's begin with number 2.<br><br>")
        initialStep.append(f"Let's use the given number, {n}. We'll now start by writing the root. Then, we'll draw two arrows to connect the first to the root's branches or contributing elements. Starting with 2, we'll keep trying until we find a number that divides {n} perfectly. (Note that we didn't take 1 because every number can be divided by both 1 and the number itself).<br><br>")
        initialStep.append(f"{n} is the targeted number whose factors are to be determined. We have to find the first two factors of {n}. We'll check if 2 is a factor of {n} because 2 is the smallest possible number we have in our hand (Note that we didn't pick 1, since 1 and the number itself are always the two factors of the given number).<br><br>")
        initialStep.append(
            f"The target number, for which the factors should be determined, is {n}. We'll try to find such two numbers which we can multiply to get {n}. But we won't use 1 because if we use 1, we have to multiply it with {n} to obtain {n} and it won't decompose our given number. So, we'll check if 2 is a factor of {n} since it's the smallest integer we can use.<br><br>")

######################################INITIAL STEP DIVIDED BY 2#########################################################################

        initialStepBy2.append(
            f"With no leftover, {n} is divided by 2 in this instance. Therefore, the first two factors of {n} will be {primef[0]} and {left[1]}. We would continue exploring until we discovered a prime number that exactly divided {n} if it wasn't divisible by 2.")
        initialStepBy2.append(
            f"There are no leftovers when you split {n} by 2. Thus, {primef[0]} and {left[1]} will be the first two elements of {n}. If it wasn't divisible by 2, we would keep looking until we found a prime number that exactly divided {n}.")
        initialStepBy2.append(
            f"Here {n} is divided by 2, leaving no remainder. The first two components of {n} will thus be {primef[0]} and {left[1]}. If it wasn't divisible by 2, we would keep looking until a prime number was found that exactly divided {n}.")

######################################INITIAL STEP NOT DIVIDED BY 2#########################################################################

        initialStepNotBy2.append(
            f"As you can see, {n} cannot be divided by 2 without remainder. So we'll now check the next prime numbers (3, 5, 7, ...) ultil we found one that exactly divides {n}. We'll give it a shot with {primef[0]}, since {n} is neatly divisible by that number. If it wasn't divisible by {primef[0]}, we'd keep looking. So we got {primef[0]} & {left[1]} as the first two factors of {n}.")
        initialStepNotBy2.append(
            f"{primef[0]} divides {n} exactly and we get {primef[0]} & {left[1]} as two factors of {n}.")
        initialStepNotBy2.append(
            f"{n} isn’t evenly divisible by 2. So, we’ll try with {primef[0]} and it is exactly divisible by {primef[0]} giving {primef[0]} & {left[1]} as the two factors of {n}. (Note: If it wasn’t divisible by {primef[0]}, we would’ve gone to the next prime number until we find the number which divides {n} exactly.) ")
        initialStepNotBy2.append(
            f"In this case, {n} cannot be divided by 2 without remainder. But {primef[0]} divides {n} perfectly, giving us {primef[0]} and {left[1]} as two factors.")
        initialStepNotBy2.append(
            f"But 2 isn’t a factor of {n}. We'll give it a shot with {primef[0]}, since {n} is evenly divisible by that number, it is a factor of {n} along with {left[1]}. If it wasn't {primef[0]}, we'd keep looking until we found our first two factors of {n}.")
        initialStepNotBy2.append(
            f"Without a remainder, {n} cannot be divided by 2. Since {n} is easily divisible by {primef[0]}, we'll give it a go with {primef[0]} (Note: we would have to continue exploring until we found a prime number that exactly divided {n}). So, as the first two factors of {n}, we'll obtain {primef[0]} and {left[1]}.")

######################################LAST STEP#########################################################################

        lastStep = [
            f"Since {primef[len(primef)-2]} and {left[len(primef)-1]} are both prime numbers, they cannot be factored any further. With that, our factor tree is finished.",
            f"{primef[len(primef)-2]} & {left[len(primef)-1]} are prime numbers. So, the process ends here & we got our prime factors. Else, we had to continue the process until every branch of the tree ultimately ended as a prime number.",
            f"Both {primef[len(primef)-2]} and {left[len(primef)-1]} are prime numbers, so we won’t get anything else rather than 1 & the number itself by factoring them again. So, our factor tree is completed.",
            f"{primef[len(primef)-2]} & {left[len(primef)-1]} are the two factors of {left[len(primef)-2]}, both of which are prime numbers. This concludes the procedure, and we now have our prime factors. If not, we were to keep going until each branch of the tree resulted in a prime number.",
            f"Since {primef[len(primef)-2]} and {left[len(primef)-1]} are both prime numbers, it cannot be factored any further. With that, our factor tree is finished.",
            f"It cannot be factored further because {primef[len(primef)-2]} & {left[len(primef)-1]} are both prime numbers. Our factor tree is complete at this point."
        ]

######################################END#########################################################################
        end = [
            f"From the diagram we get {str_primef} as the prime factors of {n} as those factors can’t be factorized further. <br>We can express like this: {n} = {multi_primef}<br><br><strong>Note: we need to factorize them until all the factors become prime numbers.</strong>",
            f"Now express them as the conventional form: {n} = {multi_primef}<br><br><strong>Note : We didn’t use 1 because it is neither a prime number nor divisible further.</strong>",
            f"From the diagram we get {str_primef} as the prime factors of {n}. <br> We can express like this: {n} = {multi_primef}<br><br><strong>Note: we need to factorize them until all the factors become prime numbers.</strong>",
            f"We can express like this: {n} = {multi_primef}<br><br><strong>Note: we need to factorize them until all the factors become prime numbers.</strong>",
            f"From the diagram we get {str_primef} as the prime factors of {n} as those factors can’t be factorized further.<br> We can express like this: {n} = {multi_primef}<br><br><strong>Note: we need to factorize them until all the factors become prime numbers.</strong>",
            f"Now, we have to look at those numbers which are the top of the branches because those are our prime factors. So, {str_primef} are our prime factors obtained from the factor tree.<br>We can express like this: {n} = {multi_primef}<br><br><strong>Note: we need to factorize them until all the factors become prime numbers.</strong>"
        ]

        h4_step = "Step 1"
        content += self.wp_h4(h4_step)
        content += self.image_upload(treeImages[0])

        if primef[0] == 2:
            content += self.wp_paragraph(random.choice(initialStep) +
                                         random.choice(initialStepBy2))
        else:
            content += self.wp_paragraph(random.choice(initialStep) +
                                         random.choice(initialStepNotBy2))

        content += self.link_previous(self.numbers, self.index)

        if len(primef) > 1:
            for j in range(1, len(primef)-1):
                h4_step = f"Step {j+1}"
                content += self.wp_h4(h4_step)
                content += self.image_upload(treeImages[j])

                # loopInsideRandomString = [
                #     f"Given that {primef[j-1]} is prime whereas {left[j]} is not, we can factorize {left[j]} in the same way we did before. The two components of {left[j]} are hence {primef[j]} and {left[j+1]}.",
                #     f"As {primef[j-1]} is also a prime number, and so, we only need to find the next two factors of {left[j]}. The two factors of {left[j]} are {primef[j]} & {left[j+1]}.",
                #     f"As {primef[j-1]} is a prime number but {left[j]} isn’t, we’ll factorize {left[j]} like the previous one. We’ll get {primef[j]} and {left[j+1]} as the two factors of {left[j]}.",
                #     f""
                #     f"As {primef[j-1]} is a prime number, it is also our first prime factor. Whereas {left[j]} is not, so we’ve to factorize {left[j]} in the same way we did it for {left[j-1]}. The two components of {left[j]} are hence {primef[j]} and {left[j+1]}.",
                #     f"{primef[j-1]} is a prime number but {left[j]} is not. Thus we must factorize {left[j]} similarly to how we did for {left[j-1]}. Thus, {primef[j]} & {left[j+1]} are the two factors of {left[j]}."
                # ]
                loopInsideRandomString = [
                    f"{primef[j-1]} is a prime factor but {left[j]} is not. So factorize {left[j]}, which gives {primef[j]} and {left[j+1]}.",
                    f"As {primef[j-1]} is again a prime factor so focus on the non-prime factor number {left[j]} as I mentioned earlier. Factorizing it gives {primef[j]} and {left[j+1]}.",
                    f"Factorizing the non-prime factor gives {primef[j]} and {left[j+1]}",
                    f"Repeating the process, we get {primef[j]} and {left[j+1]} as the factors of {left[j]} (the non-prime number).",
                    f"Next, we get {primef[j]} and {left[j+1]} by factorizing {left[j]} (very easy process, ain't it?).",
                    f"As {primef[j-1]} is a prime number, ignore it and factorize the non-prime number {left[j]}, which yields {primef[j]} and {left[j+1]}.",
                    f"Continuing the process, we now get {primef[j]} and {left[j+1]} by factorizing the non-prime number {left[j]}."
                ]
                content += self.wp_paragraph(
                    random.choice(loopInsideRandomString))

            h4_step = f"Step {len(primef)}"
            content += self.wp_h4(h4_step)
            # content+=self.image_upload(treeImages[])
            content += self.wp_paragraph(random.choice(lastStep))

        content += self.wp_paragraph(random.choice(end))

        return content


############################################################################################################################
# Divider
############################################################################################################################


class DivisionMethod:
    def __init__(self, n, numbers, index, divisionImages):
        self.n = n
        self.numbers = numbers
        self.index = index
        self.divisionImages = divisionImages
        # self.content = self.divisionSteps()

    def authenticate(self):
        user = "Rahi"
        password = "t5nC 34nz obVc BUzM c1Nt KQnK"
        creds = user + ':' + password
        cred_token = base64.b64encode(creds.encode())
        header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}
        return header

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

    def image_upload(self, path):
        header = self.authenticate()
        url = 'https://calculator4engineers.com/wp-json/wp/v2'
        media = {'file': open(path, 'rb')}
        image = requests.post(url+'/media', headers=header, files=media)
        post_id = json.loads(image.content.decode('utf-8'))['id']
        image_link = image.json()['guid']['rendered']
        locString = f"<!-- wp:image {{\"id\":{str(post_id)},\"sizeSlug\":\"full\",\"linkDestination\":\"none\" }} -->"
        locString += f"<figure class=\"wp-block-image size-full\"><img src=\"{image_link}\" alt=\"\" class=\"wp-image-{str(post_id)}\"/></figure>"
        locString += "<!-- /wp:image -->"
        # print(f"{image_link}\n")
        code = locString
        
        return code

    def link_previous(self, numbers, index):
        code = self.wp_paragraph(
            "<strong> Check the first step of these prime factorization examples to better understand how this step is done:</strong>")
        if index == 0:
            pass
        elif index == 1:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li></ul><!-- /wp:list -->"
        elif index == 2:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-2]}/\">Prime factorization of {numbers[index-2]}</a></li></ul><!-- /wp:list -->"
        else:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-1]}/\">Prime factorization of {numbers[index-1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-2]}/\">Prime factorization of {numbers[index-2]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/{numbers[index-3]}/\">Prime factorization of {numbers[index-3]}</a></li></ul><!-- /wp:list -->"
        return code

    def link_next(self, numbers, index):
        code = self.wp_paragraph(
            "<strong>Check the first step of these prime factorization examples to better understand how this step is done:</strong>")
        if len(numbers)-1 == index:
            pass
        elif index == len(numbers)-2:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li></ul><!-- /wp:list -->"
        elif index == len(numbers)-3:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+2]}/\">Prime factorization of {numbers[index+2]}</a></li></ul><!-- /wp:list -->"
        else:
            code += f"<!-- wp:list --><ul><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+1]}/\">Prime factorization of {numbers[index+1]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+2]}/\">Prime factorization of {numbers[index+2]}</a></li><li><a href=\"https://calculator4engineers.com/prime-factorization/prime-factorization-of-{numbers[index+3]}/\">Prime factorization of {numbers[index+3]}</a></li></ul><!-- /wp:list -->"

        return code

    def wp_h3(self, text):
        return f"<!-- wp:heading {{\"level\":3}} --><h3>{text}</h3><!-- /wp:heading -->"

    def wp_h4(self, text):
        return f"<!-- wp:heading {{\"level\":4}} --><h4>{text}</h4><!-- /wp:heading -->"

    def wp_paragraph(self, text):
        return f"<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->"

    def divisionSteps(self):
        n = self.n
        # index = self.index

        primef, left, str_primef, multi_primef = self.primeFactors(n)
        initialStep = []
        initialStepBy2 = []
        initialStepNotBy2 = []
        lastStep = []
        end = []
        divisionImages = self.divisionImages
        content = ""

######################################INITIAL STEP#########################################################################

        # initialStepBy2 = [
        #     f"Let’s find out the prime factors of {n} by division method. First we’ll divide the {n} by the smallest prime number 2. And 2 can easily divide {n}. So, we have to move towards the next one. {primef[1]} can divide {left[1]} evenly. So, we’ll divide it by {primef[1]} and get {left[2]} as the quotient.",
        #     f"To find the prime factors, first write the number {n} on the paper and check if it is divisible by the smallest prime number which is certainly 2 and exactly divides {n} which gives us a quotient of {left[1]}. After that we would look for the next one. Remember the divisor must be a prime number. In the next case {left[1]}, it is evenly divisible by {primef[1]}. The quotient will be {left[2]} after dividing by {primef[1]}.",
        #     f"Let’s find out the prime factors of {n} by division method. Divide {n} by 2 as it is the smallest prime number. It accurately divides {n}. So next, we would try with {primef[1]} as it is the next prime number which can divide {left[1]} evenly and we’ll get {left[2]} as the quotient.",
        #     f"Let’s implement the division method on {n} to find out its prime factors. First we’ll try to divide the {n} by 2 as 2 is the smallest prime number. Since 2 can exactly divide {n} with giving us a quotient of {left[1]}, we’ll then try with {primef[1]} for this quotient as {primef[1]} is the next prime number which can divide {left[1]} evenly giving {left[2]} as the quotient."

        # ]
        initialStepBy2 = [
            f"Let’s find out the prime factors of {n} by division method. First we’ll divide {n} by the smallest prime number 2. And 2 can easily divide {n}. This gives us {left[1]} as a quotient. So, we have to move towards the next one.",
            f"To find the prime factors, first write the number {n} on the paper and check if it is divisible by the smallest prime number which is certainly 2 and exactly divides {n} which gives us a quotient of {left[1]}. After that, we would look for the next one. Remember the divisor must be a prime number.",
            f"Let’s find out the prime factors of {n} by division method. Divide {n} by 2 as it is the smallest prime number. It divides {n} without any leftover.",
            f"Let’s implement the division method on {n} to find out its prime factors. First we’ll try to divide {n} by 2 as 2 is the smallest prime number. Here 2 can exactly divide {n} with giving us a quotient of {left[1]}. W’ll continue looking for next prime number when the quotient is not 1.",
            f"To find the first prime factor of {n}, divide it by the smallest prime factor 2. In this case, 2 divides {n} with no leftover, so this is our first prime number. If 2 couldn't exactly divide {n}, then we would use the next prime number one by one (3, 5, 7, 11, ...) to see which one could divide without any leftover.",
            f"Divide the target number {n} by the prime numbers 2, 3, 5, 7, ... The smallest prime number that can divide {n} without any fraction quotient is the first prime number we're looking for."
        ]

        initialStepNotBy2 = [
            f"Let’s find out the prime factors of {n} by division method. First we’ll divide {n} by the smallest prime number 2. But 2 can’t divide {n} exactly. So, we have to move towards the next one. As you can guess, no smaller prime number than {primef[0]} can divide {left[0]} evenly. By dividing {n} by {primef[0]}, we get {left[1]} as the quotient.",
            f"To find the prime factors, first write the number {n} on the paper and check if it is divisible by the smallest prime number which is certainly 2. If it isn’t, then go for the next one. Remember the divisor must be a prime number & we should start from the smallest. In case {n}, it is evenly divisible by {primef[0]}. The quotient will be {left[1]} after dividing by {primef[0]}.",
            f"Write the number {n} down first to find its prime factors, then see if it can be divided by the smallest prime number, which is definitely 2. If 2 doesn't divide {n} precisely, move on to the following. Keep in mind that we must begin with the smallest divisor and it has to be a prime number. The number {n} can be divided by {primef[0]} evenly to obtain the quotient of {left[1]}.",
            f"Let’s implement the division method on {n} to find out its prime factors. First we’ll try to divide the {n} by 2 as 2 is the smallest prime number. But 2 can’t divide {n} exactly. So, we’ll try with {primef[0]} this time as {primef[0]} is the next prime number which can divide {n} evenly giving {left[1]} as the quotient.",
            f"Let's use the division method to find the prime factors of {n}. {primef[0]} is the smallest prime number which can divide {n} exactly. So our quotient will be {left[1]}.",
            f"Use the figure to find the prime factors using division method. See if {n} can be divided by 2. Here, it's not. So we'll check the next prime number (2, 3, 5, 7, ...). No prime number smaller than {primef[0]} can divide {n} exactly, so {primef[0]} is our first prime number which gives {left[1]} as the quotient to find the next prime number."
            f"Divide {n} by the prime numbers 2, 3, 5, 7, etc. See which smallest prime number can divide {n} without any fraction quotient. In this case, {primef[0]} is our first prime number which gives the quotient {left[1]}. We'll continue doing the same until the quotient becomes 1."
        ]

######################################INITIAL STEP DIVIDED BY 2#########################################################################


######################################INITIAL STEP NOT DIVIDED BY 2#########################################################################


######################################LAST STEP#########################################################################

        lastStep = [
            f"Being a prime, {left[len(primef)-1]} can be evenly divided only by itself and the quotient will become 1. A prime factorization of {n} would include all of its divisors.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>",
            f"As {left[len(primef)-1]} is a prime number, the smallest & only prime number to divide {left[len(primef)-1]} exactly is {left[len(primef)-1]} itself and leaves 1 as quotient. So, we found the quotient 1 hence the division method is done. <br><br> We got {str_primef} as the prime factors of {n}.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>",
            f"As {left[len(primef)-1]} is a prime number, it can be divided evenly only by itself. Each divisor is a prime {n} factor. The result of multiplying all the divisors is {n}.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>",
            f"Due to the fact that {left[len(primef)-1]} is a prime number, the only prime number that can divide it exactly is {left[len(primef)-1]} (prime numbers can only be divided by 1 and the number itself). So, we found quotient 1 and completed the division procedure.  The prime factors are the divisors used to divide the number and its quotients.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>",
            f"Being a prime, {left[len(primef)-1]} can be evenly divided only by itself and the quotient will become 1. A prime factorization of {n} would include all of its divisors.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>",
            f"Being a prime, {left[len(primef)-1]} can be evenly divided only by itself and the quotient will become 1. So, the process stops here. All the divisors are our prime factors: {str_primef}.<br><strong>Note: We’ll have to repeat the process until the quotient becomes 1.</strong>"
        ]

######################################END#########################################################################

        h4_step = "Step 1"
        content += self.wp_h4(h4_step)
        content += self.image_upload(divisionImages[0])

        if primef[0] == 2:
            content += self.wp_paragraph(random.choice(initialStepBy2))
            # phase2 = 2
            # if len(primef) > 2:
            #     for j in range(phase2, len(primef)-1):
            #         h4_step = f"Step {j}"
            #         content += self.wp_h4(h4_step)
            #         content += self.image_upload(divisionImages[j])

            #         loopInsideRandomString = [
            #             f"Now we’ll repeat the exact process for the quotient also. We can divide it by {primef[j]} and {left[j+1]} will be the quotient this time.",
            #             f"We have to divide the quotient this time by the smallest prime number. {primef[j]} is the smallest prime number we’re looking for to divide the quotient exactly and it offers {left[j+1]} as the quotient this time.",
            #             f"We'll now carry out the exact same procedure for the {left[j]}. We can divide {left[j]} by {primef[j]} and {left[j+1]} will be the quotient this time.",
            #             f"Now, divide the quotient by the smallest prime number that it can be divided by. The smallest prime number we need to divide the quotient exactly is {primef[j]}, and it this time provides {left[j+1]} as the quotient.",
            #             f"We’ll repeat the same process for {left[j]} now. We can divide it by {primef[j]} and we’ll get {left[j+1]} as a quotient.",
            #             f"Now we’ll divide {left[j]} by {primef[j]} as it is the smallest prime number to divide it exactly. {left[j+1]} is the quotient."
            #         ]

            #         content += self.wp_paragraph(
            #             random.choice(loopInsideRandomString))

            #     h4_step = f"Step {len(primef)-1}"
            #     content += self.wp_h4(h4_step)
            #     content += self.image_upload(
            #         divisionImages[len(divisionImages)-1])

            #     content += self.wp_paragraph(random.choice(lastStep))

        else:
            content += self.wp_paragraph(random.choice(initialStepNotBy2))
            # phase2 = 1
            # if len(primef) > 1:
            #     for j in range(phase2, len(primef)-1):
            #         h4_step = f"Step {j+1}"
            #         content += self.wp_h4(h4_step)
            #         content += self.image_upload(divisionImages[j])

            #         loopInsideRandomString = [
            #             f"Now we’ll repeat the exact process for the quotient also. We can divide it by {primef[j]} and {left[j+1]} will be the quotient this time.",
            #             f"We have to divide the quotient this time by the smallest prime number. {primef[j]} is the smallest prime number we’re looking for to divide the quotient exactly and it offers {left[j+1]} as the quotient this time.",
            #             f"We'll now carry out the exact same procedure for the {left[j]}. We can divide {left[j]} by {primef[j]} and {left[j+1]} will be the quotient this time.",
            #             f"Now, divide the quotient by the smallest prime number that it can be divided by. The smallest prime number we need to divide the quotient exactly is {primef[j]}, and it this time provides {left[j+1]} as the quotient.",
            #             f"We’ll repeat the same process for {left[j]} now. We can divide it by {primef[j]} and we’ll get {left[j+1]} as a quotient.",
            #             f"Now we’ll divide {left[j]} by {primef[j]} as it is the smallest prime number to divide it exactly. {left[j+1]} is the quotient."
            #         ]
            #         content += self.wp_paragraph(
            #             random.choice(loopInsideRandomString))

            #     h4_step = f"Step {len(primef)}"
            #     content += self.wp_h4(h4_step)
            #     content += self.image_upload(
            #         divisionImages[len(divisionImages)-1])
            #     content += self.wp_paragraph(random.choice(lastStep))
        content += self.link_next(self.numbers, self.index)
        if len(primef) > 1:
            for j in range(1, len(primef)-1):
                h4_step = f"Step {j+1}"
                content += self.wp_h4(h4_step)
                content += self.image_upload(divisionImages[j])

                # loopInsideRandomString = [
                #     f"Now we’ll repeat the exact process for the quotient also. We can divide it by {primef[j]} and {left[j+1]} will be the quotient this time.",
                #     f"We have to divide the quotient this time by the smallest prime number. {primef[j]} is the smallest prime number we’re looking for to divide the quotient exactly and it offers {left[j+1]} as the quotient this time.",
                #     f"We'll now carry out the exact same procedure for the {left[j]}. We can divide {left[j]} by {primef[j]} and {left[j+1]} will be the quotient this time.",
                #     f"Now, divide the quotient by the smallest prime number that it can be divided by. The smallest prime number we need to divide the quotient exactly is {primef[j]}, and it this time provides {left[j+1]} as the quotient.",
                #     f"We’ll repeat the same process for {left[j]} now. We can divide it by {primef[j]} and we’ll get {left[j+1]} as a quotient.",
                #     f"Now we’ll divide {left[j]} by {primef[j]} as it is the smallest prime number to divide it exactly. {left[j+1]} is the quotient."
                # ]
                loopInsideRandomString = [
                    f"Next, divide the quotient by the smallest prime number that it can be divided by, which is {primef[j]} in this case, and it gives {left[j+1]} as the next quotient.",
                    f"Next, the smallest prime number that can divide {left[j+1]} without any remainder is {primef[j]}. So dividing by {primef[j]}, we get {left[j+1]} as the quotient.",
                    f"Similarly, {primef[j]} can divide {left[j]} with a quotient of {left[j+1]}.",
                    f"Next, {primef[j]} can divide {left[j]} with quotient {left[j+1]}, so write that down.",
                    f"Again, {left[j]} is fully divisible by {primef[j]}, the prime number, with quotient {left[j+1]}, the non-prime number.",
                    f"Now repeat the exact process for the quotient. It can be divided by {primef[j]} and {left[j+1]} will be the quotient this time.",
                    f"Divide the quotient by the smallest prime number. {primef[j]} is the smallest prime number in this case to divide the quotient without any remainder and it yields {left[j+1]} as the quotient.",
                    f"Carry out the exact same procedure for {left[j]}. We can divide {left[j]} by {primef[j]} and {left[j+1]} will be the quotient.",
                    f"Now we’ll divide {left[j]} by {primef[j]} as it is the smallest prime number to divide it exactly. {left[j+1]} is the quotient.",
                    f"{primef[j]} is the smallest prime number in this case to divide the quotient without any remainder with a new quotient of {left[j+1]}.",
                    f"Next, {primef[j]} divides {left[j]} exactly with a quotient of {left[j+1]}.",
                    f"As you can guess, {primef[j]} is our next prime number which gives the quotient {left[j+1]}"
                ]
                content += self.wp_paragraph(
                    random.choice(loopInsideRandomString))

            h4_step = f"Step {len(primef)}"
            content += self.wp_h4(h4_step)
            content += self.image_upload(divisionImages[len(divisionImages)-1])
            content += self.wp_paragraph(random.choice(lastStep))

        return content


if __name__ == "__main__":
    n = 604
    divisionImages = generateImages(n)['DivisionFiles']
    numbers = [604]
    
    i = 0
    divisionSteps = DivisionMethod(
        n, numbers, i, divisionImages).divisionSteps()
    postHtml = ""
    # print(divisionSteps)