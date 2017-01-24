from nltk.compat import python_2_unicode_compatible

# printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    # Count the number of children of a particular word
    @staticmethod
    def count_dependencies_number(idx, arcs):
        dep_left_count = 0
        dep_right_count = 0
        for (wi, r, wj) in arcs:
            if wi == idx:
                if(wj > wi):
                    dep_right_count += 1
                if(wi > wj):
                    dep_left_count += 1
        dep_left_number = str(dep_left_count)
        dep_right_number = str(dep_right_count)
        return dep_left_number, dep_right_number

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        # global printed
        # if not printed:
        #     print("This is not a very good feature extractor!")
        #     printed = True

        # an example set of features:
        if stack:
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

            # Implement CPOSTAG feature
            if 'ctag' in token and FeatureExtractor._check_informative(token['ctag']):
                result.append('STK_0_CPOSTAG_' + token['ctag'])

            # Implement POSTAG feature
            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                result.append('STK_0_POSTAG_' + token['tag'])

            # Implement LEMMA feature
            if 'lemma' in token and FeatureExtractor._check_informative(token['lemma']):
                result.append('STK_0_LEMMA_' + token['lemma'])

            # Left most, right most dependency of stack[0]
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most)

            # The number of children of stack[0], divided into left children and right children
            dep_left_number, dep_right_number = FeatureExtractor.count_dependencies_number(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_number):
                result.append('STK_0_LDEPS_' + dep_left_number)
            if FeatureExtractor._check_informative(dep_right_number):
                result.append('STK_0_RDEPS_' + dep_right_number)

            # POSTAG of stack[1]
            if len(stack) > 1:
                stack_idx1 = stack[-2]
                token = tokens[stack_idx1]
                if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                    result.append('STK_1_POSTAG_' + token['tag'])

        if buffer:
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

            # Implement CPOSTAG feature
            if 'ctag' in token and FeatureExtractor._check_informative(token['ctag']):
                result.append('BUF_0_CPOSTAG_' + token['ctag'])

            # Implement POSTAG feature
            if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                result.append('BUF_0_POSTAG_' + token['tag'])

            # Implement LEMMA feature
            if 'lemma' in token and FeatureExtractor._check_informative(token['lemma']):
                result.append('BUF_0_LEMMA_' + token['lemma'])

            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

            # The number of children of buffer[0], divided into left children and right children
            dep_left_number, dep_right_number = FeatureExtractor.count_dependencies_number(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_number):
                result.append('BUF_0_LDEPS_' + dep_left_number)
            if FeatureExtractor._check_informative(dep_right_number):
                result.append('BUF_0_RDEPS_' + dep_right_number)

            if len(buffer) > 1:
                buffer_idx1 = buffer[1]
                token = tokens[buffer_idx1]
                if FeatureExtractor._check_informative(token['word'], True):
                    result.append('BUF_1_FORM_' + token['word'])

                # POSTAG of buffer[1]
                if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                    result.append('BUF_1_POSTAG_' + token['tag'])

            # POSTAG of buffer[2]
            if len(buffer) > 2:
                buffer_idx2 = buffer[2]
                token = tokens[buffer_idx2]
                if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                    result.append('BUF_2_POSTAG_' + token['tag'])

            # POSTAG of buffer[3]
            if len(buffer) > 3:
                buffer_idx3 = buffer[3]
                token = tokens[buffer_idx3]
                if 'tag' in token and FeatureExtractor._check_informative(token['tag']):
                    result.append('BUF_3_POSTAG_' + token['tag'])

        # Distance between the word on top of the stack
        # and the first word in the input buffer
        if stack and buffer:
            # number of words intervening
            distance = str(stack[-1] - buffer[0])
            result.append('DISTANCE_' + distance)

        return result
